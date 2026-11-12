"""EDA catalogue Kaggle + compatibilité profils synthétiques.
Depuis poc/: python src/analyse_catalogue.py
Génère des figures PNG, un rapport HTML et des métriques JSON.
"""

import argparse
import html
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd


def make_bar(series: pd.Series, title: str, xlabel: str, target: Path, top: int = 12):
    counts = series.fillna("(Manquant)").astype(str).value_counts().head(top)
    fig, ax = plt.subplots(figsize=(10, max(4, len(counts) * 0.43 + 1.2)))
    counts.sort_values().plot(kind="barh", ax=ax)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("")
    fig.tight_layout()
    fig.savefig(target, dpi=140)
    plt.close(fig)


def make_missing(df: pd.DataFrame, target: Path):
    missing = (df.isna().sum() / max(len(df), 1) * 100).sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(10, 4.5))
    missing.plot(kind="barh", ax=ax)
    ax.set_title("Taux de valeurs manquantes après préparation")
    ax.set_xlabel("Pourcentage de lignes (%)")
    fig.tight_layout()
    fig.savefig(target, dpi=140)
    plt.close(fig)


def make_cross(df: pd.DataFrame, target: Path):
    tab = (
        pd.crosstab(df["category"], df["usage"].fillna("(Manquant)"), normalize="index")
        * 100
    )
    fig, ax = plt.subplots(figsize=(11, 4.6))
    img = ax.imshow(tab.to_numpy(), aspect="auto", cmap="Blues", vmin=0, vmax=100)
    ax.set_xticks(range(len(tab.columns)), tab.columns, rotation=40, ha="right")
    ax.set_yticks(range(len(tab.index)), tab.index)
    ax.set_title("Usage par famille de produits (% au sein de chaque famille)")
    fig.colorbar(img, ax=ax, label="%")
    fig.tight_layout()
    fig.savefig(target, dpi=140)
    plt.close(fig)


def profile_review(path: Path | None, cat: pd.DataFrame) -> dict:
    if path is None or not path.is_file():
        return {
            "available": False,
            "note": "CSV profils absent : passer --profiles chemin/du/csv",
        }
    profiles = pd.read_csv(path)
    result = {
        "available": True,
        "rows": len(profiles),
        "columns": list(profiles.columns),
        "missing": {c: int(profiles[c].isna().sum()) for c in profiles.columns},
        "duplicate_user_ids": (
            int(profiles["user_id"].duplicated().sum())
            if "user_id" in profiles
            else None
        ),
        "limits": [],
    }

    if "preferred_categories" in profiles:
        requested = {
            v.strip()
            for values in profiles["preferred_categories"].dropna().astype(str)
            for v in values.split("|")
        }
        present = set(cat["category"].dropna().astype(str))
        result["preferred_categories"] = sorted(requested)
        result["catalogue_categories"] = sorted(present)
        result["unmatched_categories_without_mapping"] = sorted(requested - present)
        if requested - present:
            result["limits"].append(
                "Catégories françaises des profils non alignées sur les familles Kaggle : créer un mapping explicite avant la recommandation."
            )
    if "preferred_styles" in profiles:
        result["limits"].append(
            "Styles synthétiques (chic, streetwear, etc.) non directement disponibles dans le champ usage Kaggle : ne pas assimiler automatiquement les vocabulaires."
        )
    if "budget_max_eur" in profiles:
        result["limits"].append(
            "Les budgets fictifs ne sont pas utilisables pour filtrer le vrai catalogue : prix absents de Kaggle."
        )
    if "preferred_sizes" in profiles:
        result["limits"].append(
            "Les tailles préférées ne sont pas utilisables pour filtrer le vrai catalogue : tailles absentes de Kaggle."
        )
    if "retention_until" in profiles and "created_at" in profiles:
        created = pd.to_datetime(profiles["created_at"], errors="coerce")
        retained = pd.to_datetime(profiles["retention_until"], errors="coerce")
        result["retention_days"] = sorted(
            (retained - created).dt.days.dropna().unique().astype(int).tolist()
        )
        result["limits"].append(
            "Durée fictive de 90 jours à valider avec les DPO : ce n'est pas une obligation RGPD générale."
        )
    return result


def generate(catalogue: Path, quality: Path, profiles: Path | None, output: Path):
    df = pd.read_csv(catalogue)
    output.mkdir(parents=True, exist_ok=True)
    images = output / "figures"
    images.mkdir(exist_ok=True)
    source_summary = (
        json.loads(quality.read_text(encoding="utf-8")) if quality.is_file() else None
    )
    charts = [
        ("categories", "Catégories", "category", 10),
        ("usages", "Usages", "usage", 12),
        ("types_articles", "Types d'articles", "article_type", 15),
        ("sous_categories", "Sous-catégories", "subcategory", 15),
        ("couleurs", "Couleurs", "color", 15),
    ]
    for name, title, column, top in charts:
        make_bar(df[column], title, "Nombre de produits", images / f"{name}.png", top)
    make_missing(df, images / "valeurs_manquantes.png")
    make_cross(df, images / "categories_usages.png")
    review = profile_review(profiles, df)
    metrics = {
        "catalogue_rows": len(df),
        "catalogue_columns": list(df.columns),
        "duplicates_product_id": int(df["product_id"].duplicated().sum()),
        "missing": {c: int(df[c].isna().sum()) for c in df.columns},
        "categories": df["category"].value_counts().to_dict(),
        "usage": df["usage"].value_counts().to_dict(),
        "profiles": review,
        "raw_quality_report_present": source_summary is not None,
    }
    (output / "metriques_eda.json").write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    cards = [
        ("Produits après préparation", len(df)),
        ("Doublons identifiants", metrics["duplicates_product_id"]),
        ("Champs", len(df.columns)),
        ("Profils synthétiques", review.get("rows", "Non chargés")),
    ]
    sections = "".join(
        f'<section><h2>{html.escape(title)}</h2><img src="figures/{filename}.png" alt="Graphique {html.escape(title)}"></section>'
        for filename, title in [
            ("categories", "Familles de produits"),
            ("usages", "Usages vestimentaires"),
            ("types_articles", "Types d’articles (top 15)"),
            ("sous_categories", "Sous-catégories (top 15)"),
            ("couleurs", "Couleurs (top 15)"),
            ("valeurs_manquantes", "Complétude des champs"),
            ("categories_usages", "Catégorie × usage"),
        ]
    )
    cards_html = "".join(
        f'<div class="card"><strong>{html.escape(str(value))}</strong><span>{html.escape(label)}</span></div>'
        for label, value in cards
    )
    limits = [
        "Ce rapport décrit le catalogue APRÈS préparation. Les anomalies brutes et exclusions sont consignées dans rapport_catalogue.json.",
        "La surreprésentation d’un usage peut limiter la couverture de certains besoins ; elle n’établit pas à elle seule une discrimination.",
        "Les produits Kaggle ne possèdent pas de prix ni de tailles utilisables. Les budgets et tailles des profils ne peuvent donc pas être reliés automatiquement au catalogue.",
        "Le champ 'usage' n'est pas une taxonomie complète de styles vestimentaires.",
        "Aucune photo de personne réelle n'est nécessaire pour cette démonstration.",
    ] + review.get("limits", [])
    if not source_summary:
        limits.append(
            "Rapport d'audit source absent : lancer d'abord prepare_catalogue.py."
        )
    limits_html = "".join(f"<li>{html.escape(msg)}</li>" for msg in limits)
    source_html = ""
    if source_summary:
        exclusions = source_summary.get("transformation_exclusions")
        if exclusions:
            source_html = (
                "<h2>Traçabilité des exclusions</h2><table><tr><th>Motif</th><th>Nombre</th></tr>"
                + "".join(
                    f"<tr><td>{html.escape(str(k))}</td><td>{v}</td></tr>"
                    for k, v in exclusions.items()
                )
                + "</table>"
            )
        else:
            source_html = "<p>Rapport source ancien format : détails des exclusions non disponibles. Relancer le script prepare_catalogue.py fourni.</p>"
    document = f"""<!doctype html><html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>FashMatch — EDA Catalogue</title>
    <style>body{{font-family:Arial,sans-serif;margin:0;background:#f4f6fa;color:#17223b}}header{{background:#132345;color:white;padding:35px max(20px,calc((100% - 1040px)/2))}}main{{max-width:1040px;margin:auto;padding:24px}}.metrics{{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}}.card,section{{background:white;padding:20px;border-radius:12px;box-shadow:0 1px 5px #dce0e8;margin-bottom:18px}}.card strong{{display:block;font-size:28px}}.card span{{color:#667}}img{{width:100%;height:auto}}table{{border-collapse:collapse;background:white;width:100%}}td,th{{text-align:left;border-bottom:1px solid #ddd;padding:9px}}li{{margin-bottom:8px}}h2{{margin-top:0}}</style></head><body>
    <header><h1>FashMatch — Analyse exploratoire du catalogue</h1><p>POC Data Engineering × DPO | Données publiques produits et profils fictifs</p></header><main>
    <div class="metrics">{cards_html}</div><section><h2>Ce que l'on peut conclure</h2><p>Le catalogue contient {len(df):,} références après préparation. Les graphiques caractérisent sa répartition et les données manquantes. La qualité finale doit être interprétée à la lumière des rejets et des exclusions de la source.</p></section>
    {sections}<section>{source_html}</section><section><h2>Limites et décisions à valider</h2><ul>{limits_html}</ul></section><p><small>Rapport généré à partir des fichiers locaux. Aucune donnée réelle d'utilisateur utilisée.</small></p></main></body></html>"""
    (output / "rapport_eda.html").write_text(document, encoding="utf-8")
    print(f"Rapport EDA : {output / 'rapport_eda.html'}")
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--catalogue", type=Path, default=Path("data/processed/catalogue_fashmatch.csv")
    )
    parser.add_argument(
        "--quality", type=Path, default=Path("data/processed/rapport_catalogue.json")
    )
    parser.add_argument(
        "--profiles",
        type=Path,
        default=Path("data/synthetic/profils_utilisateurs_SYNTHETIQUES.csv"),
    )
    parser.add_argument("--output", type=Path, default=Path("reports/catalogue"))
    args = parser.parse_args()
    generate(args.catalogue, args.quality, args.profiles, args.output)
