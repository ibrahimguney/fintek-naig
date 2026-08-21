import json
import pandas as pd
from statsmodels.miscmodels.ordinal_model import OrderedModel
from common import ROOT, PROCESSED, TABLES

DATA = PROCESSED / "cbdc_findex_merged_2021.csv"
df = pd.read_csv(DATA)

focal_vars = [
    "account_ownership_2021",
    "digital_payment_2021",
    "online_bill_payment_2021",
]
controls = ["borrowed_any_2021", "log_adult_population"]
rows = []
summary = {}

for link in ["probit", "logit"]:
    summary[link] = {}
    for var in focal_vars:
        cols = ["project_score_overall", var, *controls]
        d = df[cols].dropna().copy()
        X = d[[var, *controls]].copy()
        X = (X - X.mean()) / X.std()
        y = d["project_score_overall"].astype(int)
        res = OrderedModel(y, X, distr=link).fit(method="bfgs", disp=False)
        summary[link][var] = {
            "coef": float(res.params[var]),
            "se": float(res.bse[var]),
            "p": float(res.pvalues[var]),
            "n": int(res.nobs),
            "aic": float(res.aic),
        }
        for term in [var, *controls]:
            rows.append({
                "link": link,
                "specification": var,
                "term": term,
                "coef": float(res.params[term]),
                "std_err": float(res.bse[term]),
                "p_value": float(res.pvalues[term]),
                "n": int(res.nobs),
                "aic": float(res.aic),
            })

pd.DataFrame(rows).to_csv(TABLES / "table2_ordered_models.csv", index=False)
(ROOT / "outputs" / "ordered_models_summary.json").write_text(
    json.dumps(summary, indent=2), encoding="utf-8"
)
print("Ordered probit/logit models completed.")
