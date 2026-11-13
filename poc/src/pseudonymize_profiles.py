"""FashMatch J2 — HMAC pseudonymisation, table d'identité isolée du CSV exploitable.
Depuis poc/: python src/pseudonymize_profiles.py
IMPORTANT : une pseudonymisation n'est PAS une anonymisation RGPD.
"""
import argparse
import csv
import hashlib
import hmac
import os
import secrets
from pathlib import Path

PII = {"user_id", "first_name", "last_name", "email"}


def read_csv(path):
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path, rows, columns):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def load_key(key_file: Path):
    """Clé conservée hors Git dans data/private, jamais dans les rapports."""
    if key_file.is_file():
        key = bytes.fromhex(key_file.read_text(encoding="ascii").strip())
        if len(key) < 32:
            raise ValueError("Clé de pseudonymisation trop courte")
        return key
    key_file.parent.mkdir(parents=True, exist_ok=True)
    key = secrets.token_bytes(32)
    # Création exclusive pour ne pas écraser une clé préexistante.
    try:
        with key_file.open("x", encoding="ascii") as handle:
            handle.write(key.hex())
        if os.name == "posix":
            key_file.chmod(0o600)
    except FileExistsError:
        return load_key(key_file)
    return key


def pseudonymize(source: Path, output: Path, mapping: Path, key_file: Path):
    rows = read_csv(source)
    if not rows:
        raise ValueError("Aucun profil à pseudonymiser")
    missing = PII - set(rows[0])
    if missing:
        raise ValueError(f"Identifiants manquants : {sorted(missing)}")
    key = load_key(key_file)
    pseudonyms, correspondence, seen = [], [], set()
    for row in rows:
        original = row["user_id"].strip()
        if not original or original in seen:
            raise ValueError("Identifiant utilisateur vide ou dupliqué")
        seen.add(original)
        alias = "PS_" + hmac.new(key, original.encode("utf-8"), hashlib.sha256).hexdigest()[:24]
        public = {"user_id": alias}
        public.update({k: v for k, v in row.items() if k not in PII})
        pseudonyms.append(public)
        correspondence.append({
            "user_id": original, "pseudonym_id": alias,
            "first_name": row["first_name"], "last_name": row["last_name"], "email": row["email"],
            "retention_until": row.get("retention_until", ""),
        })
    public_fields = ["user_id"] + [k for k in rows[0] if k not in PII]
    write_csv(output, pseudonyms, public_fields)
    write_csv(mapping, correspondence, list(correspondence[0]))
    print(f"{len(pseudonyms)} profils pseudonymisés : {output}")
    print(f"Table de correspondance PRIVÉE : {mapping}")
    return len(pseudonyms)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=Path("data/private/profils_identifiants_SYNTHETIQUES.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/synthetic/profils_utilisateurs_SYNTHETIQUES.csv"))
    parser.add_argument("--mapping", type=Path, default=Path("data/private/correspondance_profils.csv"))
    parser.add_argument("--key-file", type=Path, default=Path("data/private/.pseudonym_key"))
    args = parser.parse_args()
    pseudonymize(args.source, args.output, args.mapping, args.key_file)
