import numpy as np
import pandas as pd
from common import RAW, PROCESSED

bis = pd.read_csv(RAW / "bis_cbdc_mar2024.csv")
bis = bis.dropna(subset=["ISO2", "project_score_overall"]).copy()
# BIS Mart 2024 dosyasında bazı ISO2 kayıtları aynı içerikle yinelenebiliyor.
# Ülke düzeyi analiz için tek kayıt tutulur.
bis = bis.sort_values(["ISO2", "project_score_overall"]).drop_duplicates(subset=["ISO2"], keep="last")

findex = pd.read_csv(RAW / "findex_selected_2021.csv")

keep_bis = [
    "ISO2", "country_name", "project_score_overall", "project_score_retail",
    "project_score_wholesale", "search_interest_normalized",
    "central_bankers_speech_stance_index_normalized",
]
keep_bis = [c for c in keep_bis if c in bis.columns]

df = bis[keep_bis].merge(findex, on="ISO2", how="inner", validate="one_to_one")

numeric = [
    "project_score_overall", "project_score_retail", "project_score_wholesale",
    "search_interest_normalized", "central_bankers_speech_stance_index_normalized",
    "pop_adult", "account_ownership_2021", "digital_payment_2021",
    "online_bill_payment_2021", "digital_merchant_payment_2021", "borrowed_any_2021",
]
for col in numeric:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

df["log_adult_population"] = np.log(df["pop_adult"].where(df["pop_adult"] > 0))
df["advanced_cbdc"] = (df["project_score_overall"] >= 2).astype(int)

order = [
    "ISO2", "country_name", "project_score_overall", "project_score_retail",
    "project_score_wholesale", "advanced_cbdc", "search_interest_normalized",
    "central_bankers_speech_stance_index_normalized", "incomegroupwb24",
    "regionwb24_hi", "pop_adult", "log_adult_population",
    "account_ownership_2021", "digital_payment_2021",
    "online_bill_payment_2021", "digital_merchant_payment_2021",
    "borrowed_any_2021",
]
df = df[[c for c in order if c in df.columns]].sort_values("ISO2")

out = PROCESSED / "cbdc_findex_merged_2021.csv"
df.to_csv(out, index=False)
print(f"Saved {len(df)} matched jurisdictions -> {out}")
