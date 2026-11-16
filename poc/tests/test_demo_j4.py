"""Tests unitaires J4 indépendants des données Kaggle réelles."""
import importlib.util
import json
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "src" / "preparer_demo_j4.py"
spec = importlib.util.spec_from_file_location("preparer_demo_j4", FILE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def test_pct():
    assert module.pct(1, 4) == 25.0
    assert module.pct(0, 0) is None


def test_consolidation_and_no_sensitive_fields(tmp_path):
    root = tmp_path
    for folder in ["data/processed", "reports/profils", "reports/catalogue"]:
        (root / folder).mkdir(parents=True, exist_ok=True)
    (root / "data/processed/rapport_catalogue.json").write_text(json.dumps({"source_rows": 5, "output_rows": 4, "categories": {"Apparel": 4}, "usage": {"Casual": 3}, "missing_values_in_output": {"color": 1}}))
    (root / "reports/profils/rapport_qualite_profils.json").write_text(json.dumps({"status": "OK", "profile_rows": 2, "catalogue_rows": 4, "duplicate_user_ids": 0, "invalid_dates": 0, "issues": [], "retention_days": [90]}))
    (root / "reports/catalogue/metriques_eda.json").write_text(json.dumps({"catalogue_rows": 4, "profiles": {"rows": 2}}))
    m = module.collect(root)
    assert m["catalogue"]["products"] == 4
    assert m["profiles"]["count"] == 2
    assert "private" not in json.dumps(m)
    assert "<html" in module.make_html(m)
    assert "3" in module.make_md(m)


def test_reports_disagree_fail_explicitly(tmp_path):
    root = tmp_path
    for folder in ["data/processed", "reports/profils", "reports/catalogue"]:
        (root / folder).mkdir(parents=True, exist_ok=True)
    (root / "data/processed/rapport_catalogue.json").write_text(json.dumps({"output_rows": 4}))
    (root / "reports/profils/rapport_qualite_profils.json").write_text(json.dumps({"catalogue_rows": 5, "profile_rows": 2}))
    (root / "reports/catalogue/metriques_eda.json").write_text(json.dumps({"catalogue_rows": 4}))
    try:
        module.collect(root)
        assert False, "Expected mismatch exception"
    except ValueError as e:
        assert "Incohérence" in str(e)
