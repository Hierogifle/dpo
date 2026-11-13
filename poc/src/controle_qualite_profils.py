"""J3 — rapport qualité du jeu de profils pseudonymisés, prêt pour les DPO."""
import argparse
import json
from datetime import date
from pathlib import Path

import pandas as pd

from journal_traitements import log_event

MANDATORY = {
    "user_id", "preferred_categories", "preferred_colors", "preferred_usages",
    "created_at", "retention_until", "synthetic",
}
FORBIDDEN = {"first_name", "last_name", "email", "budget_max_eur", "preferred_sizes", "preferred_styles"}


def analyze(profiles_path: Path, catalogue_path: Path, report_path: Path,
            strict: bool = False, log_path: Path | None = None, today: date | None = None):
    profiles = pd.read_csv(profiles_path, dtype="string")
    catalogue = pd.read_csv(catalogue_path, dtype="string")
    issues = []
    missing_fields = sorted(MANDATORY - set(profiles))
    forbidden_present = sorted(FORBIDDEN & set(profiles))
    if missing_fields:
        issues.append(f"Colonnes obligatoires absentes : {missing_fields}")
    if forbidden_present:
        issues.append(f"Champs supprimés/interdits présents : {forbidden_present}")
    if profiles.empty:
        issues.append("Aucun profil disponible")
    if any(x not in catalogue.columns for x in ("category", "color", "usage")):
        issues.append("Colonnes de vocabulaire catalogue absentes")
    duplicate_ids = int(profiles["user_id"].duplicated().sum()) if "user_id" in profiles else None
    if duplicate_ids:
        issues.append(f"Identifiants dupliqués : {duplicate_ids}")
    if "user_id" in profiles and not profiles["user_id"].fillna("").str.fullmatch(r"PS_[a-f0-9]{24}").all():
        issues.append("Certains pseudonymes ne respectent pas le format attendu")
    missing_values = {str(col): int(profiles[col].isna().sum()) for col in profiles.columns}
    for name in sorted(MANDATORY & set(profiles)):
        if missing_values[name]:
            issues.append(f"Valeurs manquantes dans {name} : {missing_values[name]}")
    unknowns = {}
    if all(c in catalogue for c in ("category", "color", "usage")):
        for profile_field, cat_field in (
            ("preferred_categories", "category"),
            ("preferred_colors", "color"),
            ("preferred_usages", "usage"),
        ):
            if profile_field not in profiles:
                continue
            known = set(catalogue[cat_field].dropna().str.strip())
            seen = {item.strip() for cell in profiles[profile_field].dropna() for item in str(cell).split("|") if item.strip()}
            unknowns[profile_field] = sorted(seen - known)
            if unknowns[profile_field]:
                issues.append(f"Valeurs non alignées {profile_field} : {unknowns[profile_field]}")
    invalid_dates = 0
    retention_days = []
    expired = 0
    if {"created_at", "retention_until"} <= set(profiles):
        created = pd.to_datetime(profiles["created_at"], errors="coerce")
        retention = pd.to_datetime(profiles["retention_until"], errors="coerce")
        invalid_dates = int((created.isna() | retention.isna() | (retention < created)).sum())
        retention_days = sorted(set((retention - created).dt.days.dropna().astype(int)))
        expired = int((retention.dt.date < (today or date.today())).sum())
        if invalid_dates:
            issues.append(f"Dates incohérentes : {invalid_dates}")
    if "synthetic" in profiles and not profiles["synthetic"].fillna("").str.lower().eq("true").all():
        issues.append("Certains profils ne sont pas explicitement marqués synthétiques")
    report = {
        "status": "OK" if not issues else "A_CORRIGER",
        "profile_rows": len(profiles), "catalogue_rows": len(catalogue),
        "duplicate_user_ids": duplicate_ids, "missing_values": missing_values,
        "forbidden_fields_present": forbidden_present, "unknown_preference_values": unknowns,
        "invalid_dates": invalid_dates, "retention_days": retention_days,
        "expired_as_of_today": expired,
        "issues": issues,
        "limitations": [
            "Le contrôle des vocabulaires ne prouve pas la qualité des recommandations.",
            "Les profils sont intégralement fictifs : ce test ne démontre pas une conformité RGPD en production.",
            "La durée de conservation est illustrative, à arbitrer avec les DPO.",
            "L'absence de noms dans le CSV ne rend pas nécessairement des données réelles anonymes.",
        ],
    }
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "# FashMatch — Rapport qualité des profils (J3)", "",
        f"**Statut : {report['status']}**", "",
        f"- Profils contrôlés : **{len(profiles)}**",
        f"- Produits de référence : **{len(catalogue)}**",
        f"- Doublons d'identifiant : **{duplicate_ids}**",
        f"- Dates incohérentes : **{invalid_dates}**",
        f"- Profils dont `retention_until` est passé : **{expired}** (date d'exécution)",
        "", "## Points à corriger",
    ]
    lines.extend(f"- {issue}" for issue in issues) if issues else lines.append("- Aucun écart détecté par les contrôles mis en œuvre.")
    lines.extend(["", "## Limites"] + [f"- {v}" for v in report["limitations"]])
    report_path.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    if log_path is not None:
        log_event("controle_qualite", "success" if not issues else "error",
                  {"checked_rows": len(profiles), "issues": len(issues)}, log_path)
    print(f"Qualité : {report['status']} — {len(profiles)} profils; {len(issues)} points à corriger")
    if strict and issues:
        raise ValueError("Contrôles qualité échoués : voir rapport")
    return report


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--profiles", type=Path, default=Path("data/synthetic/profils_utilisateurs_SYNTHETIQUES.csv"))
    parser.add_argument("--catalogue", type=Path, default=Path("data/processed/catalogue_fashmatch.csv"))
    parser.add_argument("--report", type=Path, default=Path("reports/profils/rapport_qualite_profils.json"))
    parser.add_argument("--log", type=Path, default=Path("reports/journal/traitements.jsonl"))
    parser.add_argument("--strict", action="store_true")
    args = parser.parse_args()
    analyze(args.profiles, args.catalogue, args.report, args.strict, args.log)
