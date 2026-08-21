from __future__ import annotations

import numpy as np
import pandas as pd

from common import PROCESSED, RAW, TABLES

BASE = PROCESSED / "cbdc_findex_merged_2021.csv"
WDI = RAW / "wdi_2021.csv"
WGI = RAW / "wgi_2021.csv"
OUT = PROCESSED / "cbdc_extended_2021.csv"

required = [BASE, WDI, WGI]
missing = [str(p) for p in required if not p.exists()]
if missing:
    raise FileNotFoundError(
        "Missing Phase-2 input file(s): " + ", ".join(missing) +
        ". Run analysis/08_fetch_wdi_wgi.py first."
    )

base = pd.read_csv(BASE)
wdi = pd.read_csv(WDI)
wgi = pd.read_csv(WGI)

for d in (base, wdi, wgi):
    d["ISO2"] = d["ISO2"].astype(str).str.upper().str.strip()

wdi_cols = [c for c in wdi.columns if c not in {"ISO3", "country_wb"}]
wgi_cols = [c for c in wgi.columns if c not in {"ISO3", "country_wb"}]

df = base.merge(wdi[wdi_cols], on="ISO2", how="left", validate="one_to_one")
df = df.merge(wgi[wgi_cols], on="ISO2", how="left", validate="one_to_one")

numeric_cols = [c for c in df.columns if c.endswith("_2021") or c in {"project_score_overall", "log_adult_population"}]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

if "gdp_per_capita_ppp_2021" in df.columns:
    df["log_gdp_per_capita_ppp_2021"] = np.log(
        df["gdp_per_capita_ppp_2021"].where(df["gdp_per_capita_ppp_2021"] > 0)
    )

wgi_dims = [
    "wgi_voice_accountability_2021",
    "wgi_political_stability_2021",
    "wgi_government_effectiveness_2021",
    "wgi_regulatory_quality_2021",
    "wgi_rule_of_law_2021",
    "wgi_control_corruption_2021",
]
wgi_dims = [c for c in wgi_dims if c in df.columns]
if wgi_dims:
    enough = df[wgi_dims].notna().sum(axis=1) >= 4
    df["wgi_governance_index_2021"] = df[wgi_dims].mean(axis=1).where(enough)

coverage_vars = [
    "account_ownership_2021",
    "online_bill_payment_2021",
    "log_gdp_per_capita_ppp_2021",
    "internet_users_2021",
    "domestic_credit_private_2021",
    "inflation_2021",
    "urban_population_2021",
    "fdi_net_inflows_2021",
    "wgi_governance_index_2021",
]
coverage = []
for col in [c for c in coverage_vars if c in df.columns]:
    coverage.append({
        "variable": col,
        "non_missing_n": int(df[col].notna().sum()),
        "missing_n": int(df[col].isna().sum()),
        "coverage_pct": float(100 * df[col].notna().mean()),
    })
pd.DataFrame(coverage).to_csv(TABLES / "phase2_data_coverage.csv", index=False)

df = df.sort_values("ISO2")
df.to_csv(OUT, index=False)
print(f"Saved extended dataset: {len(df)} jurisdictions -> {OUT}")
