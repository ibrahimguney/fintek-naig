import numpy as np
import pandas as pd
import statsmodels.api as sm
from common import PROCESSED, TABLES

DATA = PROCESSED / "cbdc_findex_merged_2021.csv"
df = pd.read_csv(DATA)
features = [
    "account_ownership_2021", "online_bill_payment_2021",
    "borrowed_any_2021", "log_adult_population",
]
d = df[["advanced_cbdc", *features]].dropna().copy()
X = d[features].copy()
X = (X - X.mean()) / X.std()
X = sm.add_constant(X)
y = d["advanced_cbdc"]
res = sm.Logit(y, X).fit(disp=False)

ci = res.conf_int()
out = pd.DataFrame({
    "term": res.params.index,
    "coef": res.params.values,
    "std_err": res.bse.values,
    "p_value": res.pvalues.values,
    "odds_ratio": np.exp(res.params.values),
    "or_ci_low": np.exp(ci[0].values),
    "or_ci_high": np.exp(ci[1].values),
})
out["n"] = int(res.nobs)
out["pseudo_r2"] = float(res.prsquared)
out.to_csv(TABLES / "table3_binary_logit.csv", index=False)
print("Binary logistic regression completed.")
