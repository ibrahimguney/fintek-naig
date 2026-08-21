import pandas as pd
from common import RAW

required = {
    "bis_cbdc_mar2024.csv": RAW / "bis_cbdc_mar2024.csv",
    "findex_selected_2021.csv": RAW / "findex_selected_2021.csv",
}
for name, path in required.items():
    if not path.exists():
        raise FileNotFoundError(f"Eksik veri dosyası: {path}")

bis = pd.read_csv(required["bis_cbdc_mar2024.csv"])
findex = pd.read_csv(required["findex_selected_2021.csv"])

needed_bis = {"ISO2", "country_name", "project_score_overall", "project_score_retail", "project_score_wholesale"}
needed_findex = {"ISO2", "pop_adult", "account_ownership_2021", "digital_payment_2021", "online_bill_payment_2021", "borrowed_any_2021"}

missing_bis = needed_bis - set(bis.columns)
missing_findex = needed_findex - set(findex.columns)
if missing_bis:
    raise ValueError(f"BIS dosyasında eksik sütunlar: {sorted(missing_bis)}")
if missing_findex:
    raise ValueError(f"Findex dosyasında eksik sütunlar: {sorted(missing_findex)}")

print(f"OK | BIS rows={len(bis):,} | Findex compact rows={len(findex):,}")
