from __future__ import annotations

import warnings

import numpy as np
import pandas as pd
import statsmodels.api as sm
from statsmodels.miscmodels.ordinal_model import OrderedModel
from statsmodels.stats.outliers_influence import variance_inflation_factor

from common import PROCESSED, TABLES

DATA = PROCESSED / "cbdc_extended_2021.csv"
df = pd.read_csv(DATA)

MODELS = {
    "M1_digital": [
        "account_ownership_2021",
        "online_bill_payment_2021",
        "log_adult_population",
    ],
    "M2_macro": [
        "account_ownership_2021",
        "online_bill_payment_2021",
        "log_adult_population",
        "log_gdp_per_capita_ppp_2021",
        "internet_users_2021",
        "domestic_credit_private_2021",
        "inflation_2021",
    ],
    "M3_governance": [
        "account_ownership_2021",
        "online_bill_payment_2021",
        "log_adult_population",
        "log_gdp_per_capita_ppp_2021",
        "internet_users_2021",
        "domestic_credit_private_2021",
        "inflation_2021",
        "wgi_governance_index_2021",
    ],
}

WGI_DIMS = [
    "wgi_voice_accountability_2021",
    "wgi_political_stability_2021",
    "wgi_government_effectiveness_2021",
    "wgi_regulatory_quality_2021",
    "wgi_rule_of_law_2021",
    "wgi_control_corruption_2021",
]


def zscore(frame: pd.DataFrame) -> pd.DataFrame:
    sd = frame.std(ddof=0).replace(0, np.nan)
    return (frame - frame.mean()) / sd


ordered_rows = []
fit_rows = []
for link in ["probit", "logit"]:
    for model_name, predictors in MODELS.items():
        cols = ["project_score_overall", *predictors]
        d = df[cols].dropna().copy()
        if d.empty:
            continue
        X = zscore(d[predictors])
        y = d["project_score_overall"].astype(int)
        try:
            res = OrderedModel(y, X, distr=link).fit(method="bfgs", disp=False, maxiter=1000)
        except Exception as exc:
            warnings.warn(f"Ordered {link} failed for {model_name}: {exc}")
            continue
        fit_rows.append({
            "family": f"ordered_{link}",
            "model": model_name,
            "n": int(res.nobs),
            "aic": float(res.aic),
            "bic": float(res.bic),
            "log_likelihood": float(res.llf),
        })
        for term in predictors:
            ordered_rows.append({
                "link": link,
                "model": model_name,
                "term": term,
                "coef_std": float(res.params[term]),
                "std_err": float(res.bse[term]),
                "z": float(res.tvalues[term]),
                "p_value": float(res.pvalues[term]),
                "n": int(res.nobs),
                "aic": float(res.aic),
                "bic": float(res.bic),
            })

pd.DataFrame(ordered_rows).to_csv(TABLES / "phase2_ordered_models.csv", index=False)

binary_rows = []
for model_name, predictors in MODELS.items():
    cols = ["advanced_cbdc", *predictors]
    d = df[cols].dropna().copy()
    if d.empty:
        continue
    X = sm.add_constant(zscore(d[predictors]), has_constant="add")
    y = d["advanced_cbdc"].astype(int)
    try:
        res = sm.GLM(y, X, family=sm.families.Binomial()).fit(cov_type="HC3")
    except Exception as exc:
        warnings.warn(f"Binary GLM failed for {model_name}: {exc}")
        continue
    fit_rows.append({
        "family": "binary_logit_HC3",
        "model": model_name,
        "n": int(res.nobs),
        "aic": float(res.aic),
        "bic": np.nan,
        "log_likelihood": float(res.llf),
    })
    for term in predictors:
        binary_rows.append({
            "model": model_name,
            "term": term,
            "coef_std": float(res.params[term]),
            "std_err_HC3": float(res.bse[term]),
            "z": float(res.tvalues[term]),
            "p_value": float(res.pvalues[term]),
            "odds_ratio_1sd": float(np.exp(res.params[term])),
            "n": int(res.nobs),
        })

pd.DataFrame(binary_rows).to_csv(TABLES / "phase2_binary_logit_HC3.csv", index=False)
pd.DataFrame(fit_rows).to_csv(TABLES / "phase2_model_fit.csv", index=False)

rich_predictors = MODELS["M3_governance"]
dvif = df[rich_predictors].dropna().copy()
if not dvif.empty:
    Xv = zscore(dvif)
    vif = pd.DataFrame({
        "term": Xv.columns,
        "VIF": [variance_inflation_factor(Xv.values, i) for i in range(Xv.shape[1])],
        "n": len(Xv),
    })
    vif.to_csv(TABLES / "phase2_vif.csv", index=False)

wgi_rows = []
base_controls = MODELS["M2_macro"]
for dim in [c for c in WGI_DIMS if c in df.columns]:
    predictors = [*base_controls, dim]
    d = df[["project_score_overall", *predictors]].dropna().copy()
    if d.empty:
        continue
    X = zscore(d[predictors])
    y = d["project_score_overall"].astype(int)
    try:
        res = OrderedModel(y, X, distr="probit").fit(method="bfgs", disp=False, maxiter=1000)
    except Exception as exc:
        warnings.warn(f"WGI robustness failed for {dim}: {exc}")
        continue
    wgi_rows.append({
        "wgi_dimension": dim,
        "coef_std": float(res.params[dim]),
        "std_err": float(res.bse[dim]),
        "p_value": float(res.pvalues[dim]),
        "n": int(res.nobs),
        "aic": float(res.aic),
    })

pd.DataFrame(wgi_rows).to_csv(TABLES / "phase2_wgi_dimension_robustness.csv", index=False)
print("Phase-2 econometric models completed.")
