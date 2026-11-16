"""J4-02 : consolide les rapports J1-J3, sans données personnelles ni re-exécution destructive.

Depuis poc/ : python src/preparer_demo_j4.py
Options : --root chemin_du_poc, --output reports/demo_j4
Ne lit PAS data/private, ne supprime rien, n'écrit pas dans les fichiers source.
"""
from __future__ import annotations
import argparse
import csv
import html
import json
from pathlib import Path


def load_json(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError(f"Rapport attendu absent : {path}. Exécutez d'abord python src/run_pipeline_j3.py")
    data = json.loads(path.read_text(encoding="utf-8-sig"))
    if not isinstance(data, dict):
        raise ValueError(f"Rapport JSON invalide : {path}")
    return data


def pct(a: int, b: int) -> float | None:
    return round(a * 100.0 / b, 2) if b else None


def fmt(n: int | float | None) -> str:
    return "—" if n is None else f"{n:,}".replace(",", " ")


def source_csv_summary(path: Path) -> dict:
    if not path.is_file():
        return {"present": False}
    with path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        columns = reader.fieldnames or []
        count = sum(1 for _ in reader)
    return {"present": True, "rows": count, "columns": columns}


def collect(root: Path) -> dict:
    catalogue = load_json(root / "data/processed/rapport_catalogue.json")
    profile = load_json(root / "reports/profils/rapport_qualite_profils.json")
    eda = load_json(root / "reports/catalogue/metriques_eda.json")
    rows = int(catalogue.get("output_rows", 0))
    input_rows = catalogue.get("source_rows")
    input_rows = int(input_rows) if input_rows is not None else None
    num_profiles = int(profile.get("profile_rows", 0))
    if rows != int(profile.get("catalogue_rows", rows)) or rows != int(eda.get("catalogue_rows", rows)):
        raise ValueError("Incohérence : nombre de produits différent entre les rapports J1/J3/EDA")
    if num_profiles != int(eda.get("profiles", {}).get("rows", num_profiles)):
        # EDA peut avoir été régénérée après changement du schéma; il faut documenter plutôt que masquer.
        raise ValueError("Incohérence : nombre de profils entre EDA et rapport J3")
    m = catalogue.get("missing_values_in_output", {})
    missing = {str(k): int(v) for k, v in m.items()}
    categories = {str(k): int(v) for k, v in catalogue.get("categories", {}).items()}
    usages = {str(k): int(v) for k, v in catalogue.get("usage", {}).items()}
    issues = profile.get("issues", [])
    csv_catalogue = source_csv_summary(root / "data/processed/catalogue_fashmatch.csv")
    csv_profiles = source_csv_summary(root / "data/synthetic/profils_utilisateurs_SYNTHETIQUES.csv")
    if csv_catalogue.get("present") and csv_catalogue["rows"] != rows:
        raise ValueError("Incohérence : lignes catalogue CSV / rapport")
    if csv_profiles.get("present") and csv_profiles["rows"] != num_profiles:
        raise ValueError("Incohérence : lignes profils CSV / rapport")
    return {
        "scope": "J4-02 – bilan de démonstration du POC (données synthétiques)",
        "catalogue": {"products": rows, "source_rows_parsed": input_rows,
                      "retention_rate_pct": pct(rows, input_rows) if input_rows is not None else None,
                      "categories": categories, "usages": usages,
                      "missing_by_field": missing, "total_missing_cells": sum(missing.values()),
                      "duplicate_product_ids": catalogue.get("duplicate_product_ids_before_dedup"),
                      "csv_checked": csv_catalogue["present"]},
        "profiles": {"count": num_profiles, "status": profile.get("status"),
                     "issues_detected": len(issues), "issues": issues,
                     "duplicate_user_ids": profile.get("duplicate_user_ids"),
                     "invalid_dates": profile.get("invalid_dates"),
                     "retention_days_tested": profile.get("retention_days", []),
                     "unknown_preference_values": profile.get("unknown_preference_values", {}),
                     "forbidden_fields_present": profile.get("forbidden_fields_present", []),
                     "csv_checked": csv_profiles["present"]},
        "j3": {"automated_tests_last_observed": "5 réussis (exécution rapportée par l'équipe ; relancer pytest en démonstration)",
               "purge_demo": "simulation uniquement : 0 au 2026-09-01 et 80 au 2027-02-01 (à reproduire)",
               "logging": "journal d'opérations techniques, pas journal des accès applicatifs"},
        "warnings": [
            "Les statistiques sont issues des rapports présents localement : les relancer après toute modification du pipeline.",
            "Les lignes CSV mal formées rejetées avant import ne sont pas nécessairement comptées dans source_rows_parsed.",
            "83 cellules manquantes ne signifient pas 83 produits distincts.",
            "La qualité des recommandations, l'absence de biais et la conformité RGPD en production ne sont pas démontrées.",
            "Pseudonymisation ≠ anonymisation ; noms et correspondances restent hors dépôt.",
            "Les 90 jours sont fictifs et ne constituent pas une durée légale validée.",
            "Aucune photographie ou conversation réelle n'est traitée par ce POC.",
        ]
    }


def make_html(m: dict) -> str:
    c, p = m["catalogue"], m["profiles"]
    esc = lambda x: html.escape(str(x))
    cards = [("Produits préparés", fmt(c["products"])), ("Profils fictifs", fmt(p["count"])),
             ("Anomalies profils", fmt(p["issues_detected"])), ("Doublons profils", fmt(p["duplicate_user_ids"]))]
    bars = "".join(f'<div class="barline"><span>{esc(k)}</span><div class="track"><i style="width:{min(100, 100*v/max(1,c["products"])):.2f}%"></i></div><b>{fmt(v)} ({pct(v,c["products"])} %)</b></div>' for k,v in c["categories"].items())
    usages = "".join(f'<tr><td>{esc(k)}</td><td>{fmt(v)}</td><td>{pct(v,c["products"])} %</td></tr>' for k,v in sorted(c["usages"].items(), key=lambda kv:-kv[1]))
    missing = "".join(f'<tr><td>{esc(k)}</td><td>{fmt(v)}</td><td>{pct(v,c["products"])} %</td></tr>' for k,v in c["missing_by_field"].items())
    warns = "".join(f'<li>{esc(w)}</li>' for w in m["warnings"])
    return f'''<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FashMatch – Démonstration J4</title><style>
:root{{color-scheme:light}}body{{background:#f3f5f9;color:#19263b;font:15px/1.6 system-ui,Arial;margin:0}}header{{background:#172b51;color:white;padding:44px max(22px,calc((100% - 1000px)/2))}}main{{max-width:1000px;margin:auto;padding:25px}}h1{{font-size:32px;margin:0 0 8px}}h2{{font-size:20px;margin:0 0 12px}}section{{background:white;border:1px solid #e0e5ed;border-radius:12px;padding:24px;margin:20px 0}}.cards{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:12px;margin:18px 0}}.card{{background:#fff;border:1px solid #d9e1ee;border-radius:12px;padding:16px}}.card b{{display:block;font-size:28px}}.card small{{color:#526079}}table{{width:100%;border-collapse:collapse}}td,th{{padding:8px;border-bottom:1px solid #e2e6ed;text-align:left}}.barline{{display:grid;grid-template-columns:120px 1fr 180px;align-items:center;gap:12px;margin:14px 0}}.track{{background:#e7edf8;height:16px;border-radius:99px;overflow:hidden}}.track i{{display:block;background:#315fd1;height:100%;border-radius:99px}}.note{{color:#526079}}code{{background:#edf0f6;padding:2px 5px}}@media(max-width:650px){{.barline{{grid-template-columns:1fr}}}}@media print{{body{{background:#fff}}section{{break-inside:avoid}}}}</style></head><body>
<header><h1>FashMatch · Démonstration du POC</h1><p>J4-02 · Métriques vérifiables · préparation des données, pseudonymisation, qualité et purge simulée</p></header><main>
<div class="cards">{''.join(f'<div class="card"><b>{esc(v)}</b><small>{esc(k)}</small></div>' for k,v in cards)}</div>
<section><h2>Catalogue : composition</h2>{bars}<p class="note">Sur {fmt(c['source_rows_parsed'])} lignes déjà analysées par le lecteur CSV, {fmt(c['products'])} références ont été retenues. Taux de conservation : {esc(c['retention_rate_pct'])} % (hors lignes CSV rejetées avant chargement).</p></section>
<section><h2>Usages vestimentaires</h2><table><tr><th>Usage</th><th>Produits</th><th>Part du catalogue</th></tr>{usages}</table><p class="note">Une forte domination du Casual ne constitue pas à elle seule une preuve de biais discriminatoire.</p></section>
<section><h2>Complétude</h2><table><tr><th>Champ</th><th>Valeurs manquantes</th><th>% des produits</th></tr>{missing}</table><p class="note">Total : {fmt(c['total_missing_cells'])} cellules vides, pas nécessairement autant de références distinctes.</p></section>
<section><h2>Qualité des profils</h2><p><b>Statut :</b> {esc(p['status'])} · <b>Doublons :</b> {esc(p['duplicate_user_ids'])} · <b>Dates incohérentes :</b> {esc(p['invalid_dates'])} · <b>Durée fictive :</b> {esc(', '.join(map(str,p['retention_days_tested'])))} jours.</p><p>Contrôles : champs minimisés, formats des pseudonymes, cohérence des catégories/couleurs/usages, dates et doublons.</p></section>
<section><h2>Démonstration technique J3</h2><p>{esc(m['j3']['automated_tests_last_observed'])}</p><p>{esc(m['j3']['purge_demo'])}</p><p>{esc(m['j3']['logging'])}</p><p><b>Important :</b> la démonstration de la purge est toujours sans option <code>--apply</code>.</p></section>
<section><h2>Limites et décisions DPO</h2><ul>{warns}</ul></section>
<p class="note">Rapport autonome généré depuis les rapports J1 à J3. Aucun identifiant ni fichier dans data/private n'est lu ou publié.</p></main></body></html>'''


def make_md(m: dict) -> str:
    c, p = m["catalogue"], m["profiles"]
    usage = c["usages"]
    casual = usage.get("Casual", 0)
    return f'''# FashMatch — Synthèse des métriques J4-02

## Résultats vérifiés à partir des rapports du POC

- **{fmt(c['products'])}** produits conservés ; **{fmt(c['source_rows_parsed'])}** lignes source chargées (avant filtrage, hors lignes éventuellement mal formées rejetées à la lecture).
- **{fmt(p['count'])}** profils utilisateurs entièrement fictifs pseudonymisés.
- **{p['issues_detected']}** anomalie détectée sur les profils par les contrôles disponibles ; **{p['duplicate_user_ids']}** identifiant dupliqué.
- **{fmt(casual)}** articles d'usage Casual, soit **{pct(casual, c['products'])} %** du catalogue.
- **{fmt(c['total_missing_cells'])}** cellules manquantes dans le catalogue préparé (ne pas confondre avec le nombre de lignes concernées).
- **{c['retention_rate_pct']} %** de lignes source *chargées* retenues dans le catalogue ; ne pas utiliser comme taux brut d'import sans auditer les rejets CSV.
- Durée de conservation **{', '.join(map(str,p['retention_days_tested']))} jours**, fictive et paramétrable.

## Tests et purge

L'équipe a observé **5/5 tests réussis** et deux simulations : **0 profil concerné au 01/09/2026** ; **80 au 01/02/2027**. Ces valeurs sont des constats de la précédente exécution. Relancer la suite et les simulations pendant la préparation de la démo pour les reconfirmer.

## Ce que ces métriques ne démontrent pas

- Pas de preuve d'une qualité de recommandation, de l'absence de biais ou de l'efficacité d'un système IA.
- Pas de preuve de conformité RGPD en production : aucune donnée utilisateur réelle utilisée.
- La pseudonymisation n'est pas l'anonymisation. La table de correspondance et les identités fictives sont isolées dans `data/private/` et ne doivent pas être partagées.
- Les logs J3 sont ceux du pipeline, **pas** une traçabilité complète des accès et traitements de Stella, Cabine ou Pay3x.
- La purge réelle est vérifiée par tests isolés ; ne jamais exécuter `--apply` sur la copie principale pendant la soutenance.
- Les choix d'architecture V2 et durées réelles par finalité sont des arbitrages distincts relevant de L1/L4/L5.
'''


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", type=Path, default=Path.cwd(), help="Dossier poc/")
    ap.add_argument("--output", type=Path, default=Path("reports/demo_j4"), help="Dossier de sortie, relatif à --root")
    a = ap.parse_args()
    root = a.root.resolve()
    output = a.output if a.output.is_absolute() else root / a.output
    m = collect(root)
    output.mkdir(parents=True, exist_ok=True)
    (output / "metriques_demo_j4.json").write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    (output / "rapport_demo_j4.html").write_text(make_html(m), encoding="utf-8")
    (output / "synthese_metriques_j4.md").write_text(make_md(m), encoding="utf-8")
    print(f"J4 OK : {m['catalogue']['products']} produits, {m['profiles']['count']} profils, {m['profiles']['issues_detected']} anomalies profils")
    print(f"Rapport HTML : {output / 'rapport_demo_j4.html'}")
    print("Pas de purge réelle et aucune lecture des données privées.")

if __name__ == "__main__":
    main()
