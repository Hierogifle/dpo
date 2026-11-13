"""FashMatch J2 — génère 80 profils fictifs alignés sur le catalogue Kaggle.
Depuis poc/: python src/generate_data.py
Les identités fictives restent dans data/private/, jamais publiées dans Git.
"""
import argparse
import csv
import random
from datetime import date, timedelta
from pathlib import Path

import pandas as pd

REQUIRED = {"category", "color", "usage", "product_id"}
SURNAMES = ["Martin", "Bernard", "Petit", "Robert", "Richard", "Durand", "Dubois", "Moreau", "Laurent", "Simon"]
FIRST_NAMES = ["Camille", "Alex", "Lou", "Morgan", "Charlie", "Sacha", "Noa", "Robin", "Maël", "Jules"]


def generate(catalogue: Path, destination: Path, count: int = 80, seed: int = 2026,
             reference_date: date = date(2026, 9, 1), retention_days: int = 90):
    """Ne crée QUE les profils; le catalogue synthétique V1 n'est plus utilisé."""
    if count < 1 or retention_days < 1:
        raise ValueError("count et retention_days doivent être positifs")
    df = pd.read_csv(catalogue)
    absent = REQUIRED - set(df.columns)
    if absent:
        raise ValueError(f"Colonnes catalogue manquantes : {sorted(absent)}")
    if df.empty:
        raise ValueError("Catalogue vide")
    vocab = {}
    for field in ("category", "color", "usage"):
        values = sorted({str(v).strip() for v in df[field].dropna() if str(v).strip()})
        if not values:
            raise ValueError(f"Catalogue sans vocabulaire pour {field}")
        vocab[field] = values
    rng = random.Random(seed)
    profiles = []
    for idx in range(1, count + 1):
        created = reference_date + timedelta(days=rng.randrange(60))
        first = FIRST_NAMES[(idx - 1) % len(FIRST_NAMES)]
        last = SURNAMES[(idx - 1) // len(FIRST_NAMES) % len(SURNAMES)]
        profiles.append({
            "user_id": f"U{idx:04d}",
            "first_name": first,
            "last_name": last,
            "email": f"fashmatch.fake.{idx:04d}@example.invalid",
            "preferred_categories": "|".join(rng.sample(vocab["category"], min(2, len(vocab["category"])))),
            "preferred_colors": "|".join(rng.sample(vocab["color"], min(2, len(vocab["color"])))),
            "preferred_usages": "|".join(rng.sample(vocab["usage"], min(2, len(vocab["usage"])))),
            "created_at": created.isoformat(),
            "retention_until": (created + timedelta(days=retention_days)).isoformat(),
            "synthetic": "True",
        })
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(profiles[0]))
        writer.writeheader()
        writer.writerows(profiles)
    print(f"{count} profils entièrement fictifs créés : {destination} (zone privée)")
    return profiles


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalogue", type=Path, default=Path("data/processed/catalogue_fashmatch.csv"))
    parser.add_argument("--output", type=Path, default=Path("data/private/profils_identifiants_SYNTHETIQUES.csv"))
    parser.add_argument("--count", type=int, default=80)
    parser.add_argument("--retention-days", type=int, default=90, help="Durée illustrative, à valider avec les DPO")
    args = parser.parse_args()
    generate(args.catalogue, args.output, args.count, retention_days=args.retention_days)
