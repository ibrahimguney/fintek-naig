from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
SCRIPTS = [
    "00_validate_inputs.py",
    "01_prepare_dataset.py",
    "02_descriptive.py",
    "03_ordered_models.py",
    "04_binary_logit.py",
    "05_random_forest.py",
    "06_figures.py",
    "07_turkiye_profile.py",
]

for script in SCRIPTS:
    path = ROOT / "analysis" / script
    print(f"\n=== {script} ===")
    subprocess.run([sys.executable, str(path)], check=True, cwd=ROOT)

print("\nTUM ANALIZLER BASARIYLA TAMAMLANDI.")
print(f"Tablolar: {ROOT / 'outputs' / 'tables'}")
print(f"Grafikler: {ROOT / 'outputs' / 'figures'}")
