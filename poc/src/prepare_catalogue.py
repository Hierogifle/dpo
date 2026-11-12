"""Préparation catalogue Fashion Product Images Small avec audit des exclusions.
Exécution depuis poc/: python src/prepare_catalogue.py [--limit 1000]
"""

import argparse
import csv
import json
from pathlib import Path

import pandas as pd

SOURCE_COLUMNS = [
    "id",
    "gender",
    "masterCategory",
    "subCategory",
    "articleType",
    "baseColour",
    "season",
    "year",
    "usage",
    "productDisplayName",
]
OUTPUT_COLUMNS = [
    "product_id",
    "category",
    "subcategory",
    "article_type",
    "color",
    "season",
    "usage",
    "product_name",
    "source_dataset",
]
RENAME = {
    "id": "product_id",
    "masterCategory": "category",
    "subCategory": "subcategory",
    "articleType": "article_type",
    "baseColour": "color",
    "productDisplayName": "product_name",
}
DATASET = "paramaggarwal/fashion-product-images-small"


def audit_csv_structure(path: Path) -> dict:
    """Audit des enregistrements CSV; numéros de lignes physiques (fin d'enregistrement).

    Les cas avec erreurs d'encodage et champs multilignes nécessitent une revue.
    Cette vérification ne répare jamais les enregistrements problématiques.
    """
    invalid = []
    try:
        with path.open(newline="", encoding="utf-8", errors="replace") as stream:
            reader = csv.reader(stream, strict=True)
            header = next(reader)
            expected = len(header)
            total = 0
            for fields in reader:
                total += 1
                if len(fields) != expected:
                    invalid.append(
                        {
                            "line_end": reader.line_num,
                            "expected_fields": expected,
                            "found_fields": len(fields),
                        }
                    )
    except csv.Error as error:
        return {
            "status": "audit_incomplete",
            "error": str(error),
            "malformed_rows": invalid,
        }
    return {
        "status": "ok",
        "record_count_excluding_header": total,
        "expected_field_count": expected,
        "malformed_record_count": len(invalid),
        "malformed_rows": invalid,
        "note": "Audit CSV indépendant; la stratégie de lecture Pandas est distincte.",
    }


def process(source: Path, destination: Path, report: Path, limit: int | None = None):
    if not source.is_file():
        raise FileNotFoundError(f"Fichier introuvable : {source}")
    if limit is not None and limit < 1:
        raise ValueError("--limit doit être positif")
    audit = audit_csv_structure(source)
    bad_lines = []

    def skip_bad_line(fields):
        bad_lines.append(len(fields))
        return None

    df = pd.read_csv(
        source,
        encoding="utf-8",
        encoding_errors="replace",
        engine="python",
        on_bad_lines=skip_bad_line,
    )
    missing = sorted(set(SOURCE_COLUMNS) - set(df.columns))
    if missing:
        raise ValueError(f"Colonnes obligatoires manquantes : {missing}")

    source_count = len(df)
    source_missing = {c: int(df[c].isna().sum()) for c in SOURCE_COLUMNS}
    df = df[
        [
            "id",
            "masterCategory",
            "subCategory",
            "articleType",
            "baseColour",
            "season",
            "usage",
            "productDisplayName",
        ]
    ].copy()
    df = df.rename(columns=RENAME)
    df["product_id"] = pd.to_numeric(df["product_id"], errors="coerce")
    for col in [
        "category",
        "subcategory",
        "article_type",
        "color",
        "season",
        "usage",
        "product_name",
    ]:
        df[col] = df[col].astype("string").str.strip().replace("", pd.NA)
    valid_required = df.dropna(subset=["product_id", "category", "article_type"]).copy()
    removed_missing_required = len(df) - len(valid_required)
    integer_ids = valid_required["product_id"].mod(1).eq(0)
    removed_non_integer_id = int((~integer_ids).sum())
    valid_required = valid_required.loc[integer_ids].copy()
    valid_required["product_id"] = valid_required["product_id"].astype("int64")
    duplicates = int(valid_required.duplicated(subset=["product_id"]).sum())
    valid_required = valid_required.drop_duplicates(subset=["product_id"], keep="first")
    category_mask = valid_required["category"].isin(
        ["Apparel", "Footwear", "Accessories"]
    )
    excluded_other_categories = int((~category_mask).sum())
    valid_required = valid_required.loc[category_mask].copy()
    eligible_count = len(valid_required)
    valid_required["source_dataset"] = DATASET
    valid_required = valid_required[OUTPUT_COLUMNS].sort_values("product_id")
    if limit is not None:
        valid_required = valid_required.head(limit)
    destination.parent.mkdir(parents=True, exist_ok=True)
    report.parent.mkdir(parents=True, exist_ok=True)
    valid_required.to_csv(destination, index=False, encoding="utf-8")
    report_data = {
        "source": f"https://www.kaggle.com/datasets/{DATASET}",
        "source_rows": source_count,
        "source_rows_definition": "Enregistrements acceptés par le parseur Pandas avant transformations",
        "output_rows": len(valid_required),
        "eligible_rows_before_limit": eligible_count,
        "limit": limit,
        "parsing_audit": {
            **audit,
            "pandas_rejected_bad_line_count": len(bad_lines),
            "pandas_rejected_field_counts": bad_lines,
        },
        "transformation_exclusions": {
            "missing_required_fields": int(removed_missing_required),
            "non_integer_product_id": removed_non_integer_id,
            "duplicate_product_ids": duplicates,
            "non_target_categories": excluded_other_categories,
            "limited_for_sample": eligible_count - len(valid_required),
        },
        "duplicate_product_ids_before_dedup": duplicates,
        "missing_values_in_source": source_missing,
        "missing_values_in_output": {
            c: int(valid_required[c].isna().sum()) for c in OUTPUT_COLUMNS
        },
        "categories": {
            str(k): int(v) for k, v in valid_required["category"].value_counts().items()
        },
        "usage": {
            str(k): int(v) for k, v in valid_required["usage"].value_counts().items()
        },
        "excluded_fields": ["gender", "year"],
        "notes": [
            "Aucune donnée client ni photo de personne réelle.",
            "Prix et tailles absents du catalogue public utilisé.",
            "Les lignes mal formées sont exclues, pas réparées.",
            "La licence des images et la version précise du dataset doivent être revérifiées avant diffusion.",
            "Les champs gender et year sont exclus par choix de périmètre, pas parce qu'ils sont nécessairement illicites.",
        ],
    }

    assert source_count == (
        removed_missing_required
        + removed_non_integer_id
        + duplicates
        + excluded_other_categories
        + eligible_count
    ), "Incohérence des comptes d'exclusion"
    report.write_text(
        json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"OK : {len(valid_required)} produits exportés vers {destination}")
    print(f"Rapport : {report}")
    return report_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=Path("data/raw/styles.csv"))
    parser.add_argument(
        "--output", type=Path, default=Path("data/processed/catalogue_fashmatch.csv")
    )
    parser.add_argument(
        "--report", type=Path, default=Path("data/processed/rapport_catalogue.json")
    )
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    process(args.input, args.output, args.report, args.limit)
