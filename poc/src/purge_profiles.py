"""J3 — purge cohérente de 3 CSV (public, source, correspondance) selon retention_until.
Dry-run par défaut; --apply réalise la suppression. Date limite : date < aujourd'hui.
Ne traite PAS les sauvegardes ni les données externes; démo locale uniquement.
"""
import argparse
import csv
import os
import tempfile
from datetime import date
from pathlib import Path

from journal_traitements import log_event


def load(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames:
            raise ValueError(f"CSV sans en-tête : {path}")
        return list(reader), reader.fieldnames


def staged_csv(path: Path, rows: list[dict], fields: list[str]):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix=".fashmatch-", suffix=".csv", dir=path.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            writer.writerows(rows)
        return Path(name)
    except Exception:
        Path(name).unlink(missing_ok=True)
        raise


def purge(public_path: Path, source_path: Path, mapping_path: Path,
          log_path: Path | None = None, on_date: date | None = None, apply: bool = False):
    """Évite toute modification si les 3 jeux ne sont pas cohérents.
    Écriture temporaire puis remplacement de chaque CSV; pas de transaction globale garantie.
    """
    as_of = on_date or date.today()
    public, pf = load(public_path)
    source, sf = load(source_path)
    mapping, mf = load(mapping_path)
    if not all(x in pf for x in ("user_id", "retention_until")):
        raise ValueError("Profils pseudonymisés : colonnes nécessaires manquantes")
    if "user_id" not in sf or not all(x in mf for x in ("user_id", "pseudonym_id")):
        raise ValueError("Identifiants source / correspondance manquants")
    if len({r["user_id"] for r in public}) != len(public):
        raise ValueError("Identifiants pseudonymisés dupliqués")
    if len({r["user_id"] for r in source}) != len(source):
        raise ValueError("Identifiants source dupliqués")
    ids = {row["user_id"] for row in public}
    mapping_by_alias = {row["pseudonym_id"]: row["user_id"] for row in mapping}
    if len(mapping_by_alias) != len(mapping):
        raise ValueError("Pseudonymes dupliqués dans correspondance")
    if ids != set(mapping_by_alias) or set(mapping_by_alias.values()) != {row["user_id"] for row in source}:
        raise ValueError("Jeux incohérents : purge interrompue pour éviter des orphelins")
    expired = set()
    for row in public:
        try:
            if date.fromisoformat(row["retention_until"]) < as_of:
                expired.add(row["user_id"])
        except (ValueError, TypeError):
            raise ValueError("Date de conservation invalide; aucune suppression effectuée")
    keep_public = [r for r in public if r["user_id"] not in expired]
    keep_mapping = [r for r in mapping if r["pseudonym_id"] not in expired]
    keep_source_ids = {r["user_id"] for r in keep_mapping}
    keep_source = [r for r in source if r["user_id"] in keep_source_ids]
    stats = {"input_rows": len(public), "output_rows": len(keep_public), "removed_rows": len(expired)}
    if apply and expired:
        files = [
            (public_path, keep_public, pf),
            (source_path, keep_source, sf),
            (mapping_path, keep_mapping, mf),
        ]
        staged = []
        backups = []
        try:
            # Tous les fichiers sont préparés d'abord; les originaux restent intacts en cas d'échec de staging.
            for path, rows, fields in files:
                staged.append((path, staged_csv(path, rows, fields)))
            # Backups locaux, ignorés par Git : en cas de problème, restaurer avant nouvelle exécution.
            for path, _ in staged:
                fd, copy_name = tempfile.mkstemp(prefix=".fashmatch-backup-", suffix=".csv", dir=path.parent)
                os.close(fd)
                backup = Path(copy_name)
                backup.write_bytes(path.read_bytes())
                backups.append((path, backup))
            try:
                for path, stage in staged:
                    os.replace(stage, path)
            except Exception:
                for path, backup in backups:
                    os.replace(backup, path)
                raise
        finally:
            for _, stage in staged:
                stage.unlink(missing_ok=True)
            for _, backup in backups:
                backup.unlink(missing_ok=True)
    if log_path is not None:
        log_event("purge", "success" if apply else "dry_run", stats, log_path)
    print(f"Purge {'APPLIQUÉE' if apply else 'SIMULÉE'} au {as_of.isoformat()} : {len(expired)} profils concernés")
    return stats


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profiles", type=Path, default=Path("data/synthetic/profils_utilisateurs_SYNTHETIQUES.csv"))
    parser.add_argument("--source", type=Path, default=Path("data/private/profils_identifiants_SYNTHETIQUES.csv"))
    parser.add_argument("--mapping", type=Path, default=Path("data/private/correspondance_profils.csv"))
    parser.add_argument("--log", type=Path, default=Path("reports/journal/traitements.jsonl"))
    parser.add_argument("--date", type=date.fromisoformat, help="Date de référence YYYY-MM-DD, sinon aujourd'hui")
    parser.add_argument("--apply", action="store_true", help="Applique réellement les suppressions")
    args = parser.parse_args()
    purge(args.profiles, args.source, args.mapping, args.log, args.date, args.apply)
