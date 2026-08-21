import pandas as pd
from common import PROCESSED, TABLES

DATA = PROCESSED / "cbdc_findex_merged_2021.csv"
df = pd.read_csv(DATA)

stage = (
    df["project_score_overall"]
    .value_counts(dropna=False)
    .sort_index()
    .rename_axis("project_score")
    .reset_index(name="n")
)
stage["percent"] = 100 * stage["n"] / stage["n"].sum()
stage.to_csv(TABLES / "table0_stage_distribution.csv", index=False)

vars_ = [
    "account_ownership_2021", "digital_payment_2021",
    "online_bill_payment_2021", "digital_merchant_payment_2021",
    "borrowed_any_2021", "pop_adult",
]
vars_ = [v for v in vars_ if v in df.columns]
desc = df.groupby("project_score_overall")[vars_].agg(["count", "mean", "std", "median"])
desc.to_csv(TABLES / "table1_descriptive_by_cbdc_stage.csv")

corr_vars = ["project_score_overall", *vars_]
df[corr_vars].corr(numeric_only=True).to_csv(TABLES / "table1b_correlation_matrix.csv")

print("Descriptive tables completed.")
