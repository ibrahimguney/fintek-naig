from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw"
PROCESSED = ROOT / "data" / "processed"
TABLES = ROOT / "outputs" / "tables"
FIGURES = ROOT / "outputs" / "figures"

for path in (RAW, PROCESSED, TABLES, FIGURES):
    path.mkdir(parents=True, exist_ok=True)
