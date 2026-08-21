import pandas as pd
from common import PROCESSED, TABLES

df = pd.read_csv(PROCESSED / "cbdc_findex_merged_2021.csv")
tr = df[df["ISO2"] == "TR"].copy()
if tr.empty:
    raise ValueError("Türkiye (TR) kaydı bulunamadı.")
tr.to_csv(TABLES / "table6_turkiye_empirical_profile.csv", index=False)
print(tr.to_string(index=False))
