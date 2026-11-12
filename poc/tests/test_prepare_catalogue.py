from pathlib import Path
import tempfile
import pandas as pd
from src.prepare_catalogue import process


def test_cleaning():
    with tempfile.TemporaryDirectory() as t:
        root = Path(t)
        src = root / "styles.csv"
        pd.DataFrame(
            [
                {
                    "id": 1,
                    "gender": "Men",
                    "masterCategory": "Apparel",
                    "subCategory": "Topwear",
                    "articleType": "Shirts",
                    "baseColour": "Blue",
                    "season": "Summer",
                    "year": 2012,
                    "usage": "Casual",
                    "productDisplayName": "Blue Shirt",
                },
                {
                    "id": 1,
                    "gender": "Men",
                    "masterCategory": "Apparel",
                    "subCategory": "Topwear",
                    "articleType": "Shirts",
                    "baseColour": "Blue",
                    "season": "Summer",
                    "year": 2012,
                    "usage": "Casual",
                    "productDisplayName": "Blue Shirt",
                },
                {
                    "id": 2,
                    "gender": "Women",
                    "masterCategory": "Personal Care",
                    "subCategory": "Lips",
                    "articleType": "Lipstick",
                    "baseColour": "Red",
                    "season": "Spring",
                    "year": 2017,
                    "usage": "Casual",
                    "productDisplayName": "Lipstick",
                },
            ]
        ).to_csv(src, index=False)
        process(src, root / "out.csv", root / "report.json")
        result = pd.read_csv(root / "out.csv")
        assert len(result) == 1
        assert "gender" not in result.columns
        assert "year" not in result.columns
        assert result.iloc[0]["product_id"] == 1
