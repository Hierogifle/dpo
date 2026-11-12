from pathlib import Path
import shutil
import kagglehub

POC_ROOT = Path(__file__).resolve().parents[1]

RAW_DIR = POC_ROOT / "data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

source = Path(
    kagglehub.dataset_download(
        "paramaggarwal/fashion-product-images-small", path="styles.csv"
    )
)

destination = RAW_DIR / "styles.csv"

if source.resolve() != destination.resolve():
    shutil.copy2(source, destination)

print(f"Dataset disponible : {destination}")
print(f"Taille : {destination.stat().st_size / 1024 / 1024:.2f} Mo")
