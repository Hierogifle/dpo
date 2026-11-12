"""Tests autonomes sans téléchargement Kaggle."""

import importlib.util
import tempfile
import unittest
from pathlib import Path

import pandas as pd

HERE = Path(__file__).resolve().parents[1] / "src"


def load(name):
    spec = importlib.util.spec_from_file_location(name, HERE / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PipelineTests(unittest.TestCase):
    def test_exclusions_and_outputs(self):
        mod = load("prepare_catalogue")
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            raw = base / "raw.csv"
            raw.write_text(
                "id,gender,masterCategory,subCategory,articleType,baseColour,season,year,usage,productDisplayName\n"
                "1,Men,Apparel,Topwear,Tshirts,Blue,Summer,2017,Casual,Shirt\n"
                "1,Men,Apparel,Topwear,Tshirts,Blue,Summer,2017,Casual,Shirt\n"
                "2,Men,Personal Care,Body,Soap,White,Summer,2017,Casual,Soap\n"
                "3,Men,Footwear,Shoes,Sneakers,Black,Winter,2017,Sports,Sneakers\n"
                "4,Men,Footwear,Shoes,Sneakers,Black,Winter,2017,Sports,Unexpected,Extra\n",
                encoding="utf-8",
            )
            report = mod.process(raw, base / "out.csv", base / "report.json")
            self.assertEqual(report["output_rows"], 2)
            self.assertEqual(
                report["transformation_exclusions"]["duplicate_product_ids"], 1
            )
            self.assertEqual(
                report["transformation_exclusions"]["non_target_categories"], 1
            )
            self.assertEqual(
                report["parsing_audit"]["pandas_rejected_bad_line_count"], 1
            )
            self.assertEqual(len(pd.read_csv(base / "out.csv")), 2)

    def test_eda_without_profiles(self):
        mod = load("analyse_catalogue")
        with tempfile.TemporaryDirectory() as d:
            base = Path(d)
            path = base / "catalogue.csv"
            pd.DataFrame(
                [
                    {
                        "product_id": 1,
                        "category": "Apparel",
                        "subcategory": "Topwear",
                        "article_type": "Tshirts",
                        "color": "Blue",
                        "season": "Summer",
                        "usage": "Casual",
                        "product_name": "Shirt",
                        "source_dataset": "Demo",
                    }
                ]
            ).to_csv(path, index=False)
            summary = mod.generate(path, base / "no_audit.json", None, base / "report")
            self.assertEqual(summary["catalogue_rows"], 1)
            self.assertTrue((base / "report" / "rapport_eda.html").exists())


if __name__ == "__main__":
    unittest.main()
