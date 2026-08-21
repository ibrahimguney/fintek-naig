import pandas as pd
import matplotlib.pyplot as plt
from common import PROCESSED, TABLES, FIGURES

DATA = PROCESSED / "cbdc_findex_merged_2021.csv"
df = pd.read_csv(DATA)

stage = pd.read_csv(TABLES / "table0_stage_distribution.csv")
plt.figure(figsize=(7, 4.5))
plt.bar(stage["project_score"].astype(str), stage["n"])
plt.xlabel("CBDC project score (0, 1, 2, 3)")
plt.ylabel("Jurisdictions")
plt.title("CBDC project stages in BIS–Findex sample")
plt.tight_layout()
plt.savefig(FIGURES / "figure1_cbdc_stage_distribution.png", dpi=220)
plt.close()

scores = sorted(df["project_score_overall"].dropna().unique())
groups = [df.loc[df["project_score_overall"] == s, "account_ownership_2021"].dropna().values for s in scores]
plt.figure(figsize=(7, 4.5))
plt.boxplot(groups, tick_labels=[str(int(s)) for s in scores])
plt.xlabel("CBDC project score")
plt.ylabel("Account ownership (share of adults, 2021)")
plt.title("Financial inclusion by CBDC project stage")
plt.tight_layout()
plt.savefig(FIGURES / "figure2_account_ownership_by_stage.png", dpi=220)
plt.close()

imp = pd.read_csv(TABLES / "table5_random_forest_permutation_importance.csv").sort_values("importance_mean")
plt.figure(figsize=(7, 4.5))
plt.barh(imp["feature"], imp["importance_mean"], xerr=imp["importance_sd"])
plt.xlabel("Permutation importance (ROC-AUC decrease)")
plt.title("Predictors of advanced CBDC stage")
plt.tight_layout()
plt.savefig(FIGURES / "figure3_rf_feature_importance.png", dpi=220)
plt.close()

print("Figures created.")
