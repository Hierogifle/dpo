"""Génération déterministe des jeux de données de démonstration FashMatch.
Aucune donnée personnelle réelle, aucun appel réseau.
Exécuter : python generate_data.py
"""

import csv
import random
from datetime import date, timedelta
from pathlib import Path

random.seed(2026)
OUT = Path(__file__).resolve().parents[1] / "data" / "synthetic"
OUT.mkdir(parents=True, exist_ok=True)
CATEGORIES = {
    "Haut": ["T-shirt", "Chemise", "Pull", "Sweat"],
    "Bas": ["Jean", "Pantalon", "Jupe", "Short"],
    "Veste": ["Blazer", "Manteau", "Veste légère"],
    "Chaussures": ["Baskets", "Bottines", "Mocassins"],
    "Accessoire": ["Sac", "Ceinture", "Écharpe"],
}
COLORS = ["noir", "blanc", "bleu", "beige", "gris", "vert", "marron", "rouge"]
STYLES = ["casual", "chic", "streetwear", "minimaliste", "sport"]
SEASONS = ["toutes saisons", "été", "hiver", "mi-saison"]
MATERIALS = ["coton", "lin", "laine", "polyester", "denim", "cuir synthétique"]


def write_csv(name, rows):
    with (OUT / name).open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


products = []
for i in range(1, 121):
    category = random.choice(list(CATEGORIES))
    products.append(
        {
            "product_id": f"P{i:04d}",
            "category": category,
            "subcategory": random.choice(CATEGORIES[category]),
            "color": random.choice(COLORS),
            "size": random.choice(["XS", "S", "M", "L", "XL", "TU"]),
            "style": random.choice(STYLES),
            "season": random.choice(SEASONS),
            "price_eur": round(random.uniform(12, 220), 2),
            "material": random.choice(MATERIALS),
            "source": "SYNTHETIC_DEMO_NOT_PUBLIC",
        }
    )

users = []
for i in range(1, 81):
    created = date(2026, 9, 1) + timedelta(days=random.randrange(60))
    users.append(
        {
            "user_id": f"U{i:04d}",
            "preferred_styles": "|".join(random.sample(STYLES, 2)),
            "preferred_colors": "|".join(random.sample(COLORS, 2)),
            "preferred_categories": "|".join(random.sample(list(CATEGORIES), 2)),
            "budget_max_eur": random.choice([40, 60, 80, 100, 150, 200]),
            "preferred_sizes": random.choice(["S", "M", "L", "XL"]),
            "created_at": created.isoformat(),
            "retention_until": (created + timedelta(days=90)).isoformat(),
            "synthetic": True,
        }
    )
write_csv("catalogue_DEMONSTRATION_SYNTHETIQUE.csv", products)
write_csv("profils_utilisateurs_SYNTHETIQUES.csv", users)
print(
    f"Créé : {len(products)} produits synthétiques et {len(users)} profils synthétiques"
)
