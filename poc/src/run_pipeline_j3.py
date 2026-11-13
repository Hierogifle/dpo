"""Exécution reproductible depuis poc/ de J1 (catalogue), J2 et J3 (sans purge destructrice)."""
import argparse
import subprocess
import sys
from pathlib import Path

from journal_traitements import log_event

STEPS = [
    ("generation", "prepare_catalogue.py"),
    ("generation", "generate_data.py"),
    ("pseudonymisation", "pseudonymize_profiles.py"),
    ("controle_qualite", "analyse_catalogue.py"),
    ("controle_qualite", "controle_qualite_profils.py"),
]


def run(root: Path, log_path: Path):
    for event, script in STEPS:
        target = root / "src" / script
        if not target.is_file():
            raise FileNotFoundError(f"Script requis absent : {target}")
        try:
            subprocess.run([sys.executable, str(target)], cwd=root, check=True)
        except subprocess.CalledProcessError:
            log_event(event, "error", path=log_path)
            raise
        if script != "controle_qualite_profils.py":  # celui-ci produit son propre journal
            log_event(event, "success", path=log_path)
    print("Pipeline terminé; purge non destructive à déclencher séparément.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--log", type=Path, default=Path("reports/journal/traitements.jsonl"))
    args = parser.parse_args()
    run(args.root.resolve(), (args.root / args.log).resolve() if not args.log.is_absolute() else args.log)
