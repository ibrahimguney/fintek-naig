from __future__ import annotations

import pandas as pd

from common import ROOT, TABLES

OUT = ROOT / "outputs" / "phase2_results_summary.md"


def sig(p: float) -> str:
    if p < 0.001:
        return "p < .001"
    return f"p = {p:.3f}"


lines = [
    "# Phase 2 reproducible results summary",
    "",
    "This file is generated from the analysis outputs. Interpret coefficients as associations, not causal effects.",
    "",
]

ordered_path = TABLES / "phase2_ordered_models.csv"
if ordered_path.exists():
    ordered = pd.read_csv(ordered_path)
    m3 = ordered[(ordered["link"] == "probit") & (ordered["model"] == "M3_governance")]
    if not m3.empty:
        lines += ["## Ordered probit — full specification", ""]
        for _, r in m3.sort_values("p_value").iterrows():
            lines.append(
                f"- `{r['term']}`: standardized coefficient = {r['coef_std']:.3f}, "
                f"SE = {r['std_err']:.3f}, {sig(r['p_value'])}, n = {int(r['n'])}."
            )
        lines.append("")

binary_path = TABLES / "phase2_binary_logit_HC3.csv"
if binary_path.exists():
    binary = pd.read_csv(binary_path)
    m3 = binary[binary["model"] == "M3_governance"]
    if not m3.empty:
        lines += ["## Binary logit robustness — pilot/live vs no/research", ""]
        for _, r in m3.sort_values("p_value").iterrows():
            lines.append(
                f"- `{r['term']}`: OR for a 1-SD increase = {r['odds_ratio_1sd']:.3f}, "
                f"{sig(r['p_value'])}, n = {int(r['n'])}."
            )
        lines.append("")

xgb_path = TABLES / "phase2_xgboost_cv_metrics.csv"
if xgb_path.exists():
    xgb = pd.read_csv(xgb_path).set_index("metric")
    lines += ["## XGBoost predictive performance", ""]
    for metric in ["roc_auc", "accuracy", "f1"]:
        if metric in xgb.index:
            r = xgb.loc[metric]
            lines.append(f"- {metric}: {r['mean']:.3f} ± {r['std']:.3f} across {int(r['n_folds'])} folds.")
    lines.append("")

shap_path = TABLES / "phase2_xgboost_shap_importance.csv"
if shap_path.exists():
    shap_df = pd.read_csv(shap_path).head(7)
    lines += ["## SHAP ranking", ""]
    for rank, (_, r) in enumerate(shap_df.iterrows(), 1):
        lines.append(f"{rank}. `{r['feature']}` — mean |SHAP| = {r['mean_abs_shap']:.4f}")
    lines.append("")

wgi_path = TABLES / "phase2_wgi_dimension_robustness.csv"
if wgi_path.exists():
    wgi = pd.read_csv(wgi_path).sort_values("p_value")
    lines += ["## WGI dimension robustness", ""]
    for _, r in wgi.iterrows():
        lines.append(
            f"- `{r['wgi_dimension']}`: coefficient = {r['coef_std']:.3f}, "
            f"{sig(r['p_value'])}, n = {int(r['n'])}."
        )
    lines.append("")

OUT.write_text("\n".join(lines), encoding="utf-8")
print(f"Results summary written -> {OUT}")
