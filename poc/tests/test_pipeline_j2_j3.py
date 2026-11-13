"""Tests pytest du pipeline sans toucher aux données du dépôt."""
import csv
import sys
from datetime import date
from pathlib import Path

import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from generate_data import generate
from pseudonymize_profiles import pseudonymize
from purge_profiles import purge
from controle_qualite_profils import analyze


def fixture(tmp_path):
    catalog = tmp_path / "catalogue.csv"
    pd.DataFrame({
        "product_id": [1,2,3,4],
        "category": ["Apparel", "Footwear", "Accessories", "Apparel"],
        "color": ["Black", "Blue", "Red", "Green"],
        "usage": ["Casual", "Sports", "Formal", "Casual"],
    }).to_csv(catalog, index=False)
    raw = tmp_path / "private" / "source.csv"
    dest = tmp_path / "synthetic" / "profils_utilisateurs_SYNTHETIQUES.csv"
    mapping = tmp_path / "private" / "map.csv"
    key = tmp_path / "private" / ".key"
    generate(catalog, raw, count=8, seed=2026, reference_date=date(2026, 9, 1), retention_days=90)
    pseudonymize(raw, dest, mapping, key)
    return catalog, raw, dest, mapping, key


def test_generation_compatibilite_et_minimisation(tmp_path):
    catalogue, raw, dest, mapping, key = fixture(tmp_path)
    public = pd.read_csv(dest)
    assert len(public) == 8
    assert public["user_id"].is_unique
    assert not ({"email", "first_name", "last_name", "budget_max_eur", "preferred_sizes"} & set(public))
    assert public["user_id"].str.fullmatch(r"PS_[a-f0-9]{24}").all()
    assert "preferred_usages" in public
    assert len(pd.read_csv(mapping)) == 8
    assert len(key.read_text().strip()) == 64
    before = dest.read_bytes()
    pseudonymize(raw, dest, mapping, key)
    assert dest.read_bytes() == before  # HMAC stable si clé inchangée


def test_rapport_qualite(tmp_path):
    catalogue, raw, dest, mapping, key = fixture(tmp_path)
    result = analyze(dest, catalogue, tmp_path / "report.json", strict=True, today=date(2026, 11, 1))
    assert result["status"] == "OK"
    assert result["unknown_preference_values"] == {
        "preferred_categories": [], "preferred_colors": [], "preferred_usages": [],
    }
    assert (tmp_path / "report.md").exists()


def test_purge_simulation_et_application(tmp_path):
    catalogue, raw, dest, mapping, key = fixture(tmp_path)
    before = dest.read_bytes()
    stats = purge(dest, raw, mapping, log_path=tmp_path / "log.jsonl", on_date=date(2027, 2, 1), apply=False)
    assert stats["removed_rows"] == 8
    assert dest.read_bytes() == before
    stats = purge(dest, raw, mapping, log_path=tmp_path / "log.jsonl", on_date=date(2027, 2, 1), apply=True)
    assert stats["output_rows"] == 0
    assert len(pd.read_csv(dest)) == len(pd.read_csv(raw)) == len(pd.read_csv(mapping)) == 0
    assert "@example.invalid" not in (tmp_path / "log.jsonl").read_text()


def test_purge_refuse_donnees_incoherentes(tmp_path):
    catalogue, raw, dest, mapping, key = fixture(tmp_path)
    lines = mapping.read_text().splitlines()
    mapping.write_text("\n".join(lines[:-1]) + "\n")
    before = dest.read_bytes()
    with pytest.raises(ValueError, match="incohérents"):
        purge(dest, raw, mapping, on_date=date(2027, 2, 1), apply=True)
    assert dest.read_bytes() == before


def test_controle_detecte_champ_interdit(tmp_path):
    catalogue, raw, dest, mapping, key = fixture(tmp_path)
    df = pd.read_csv(dest)
    df["email"] = "a@example.invalid"
    df.to_csv(dest, index=False)
    result = analyze(dest, catalogue, tmp_path / "report.json", today=date(2026,11,1))
    assert result["status"] == "A_CORRIGER"
    assert "email" in result["forbidden_fields_present"]
