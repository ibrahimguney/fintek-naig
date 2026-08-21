from __future__ import annotations

import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier
import shap

from common import FIGURES, PROCESSED, ROOT, TABLES

DATA = PROCESSED / "cbdc_extended_2021.csv"
df = pd.read_csv(DATA)

FEATURES = [
    "account_ownership_2021",
    "digital_payment_2021",
    "online_bill_payment_2021",
    "log_adult_population",
    "log_gdp_per_capita_ppp_2021",
    "internet_users_2021",
    "domestic_credit_private_2021",
    "inflation_2021",
    "urban_population_2021",
    "fdi_net_inflows_2021",
    "wgi_governance_index_2021",
]
FEATURES = [c for c in FEATURES if c in df.columns]
model_df = df[["advanced_cbdc", *FEATURES]].dropna(subset=["advanced_cbdc"]).copy()
X = model_df[FEATURES]
y = model_df["advanced_cbdc"].astype(int)

if y.nunique() < 2:
    raise RuntimeError("XGBoost target has fewer than two classes")

model = XGBClassifier(
    n_estimators=300,
    max_depth=3,
    learning_rate=0.03,
    subsample=0.85,
    colsample_bytree=0.85,
    min_child_weight=2,
    reg_lambda=1.0,
    objective="binary:logistic",
    eval_metric="logloss",
    random_state=42,
    n_jobs=2,
)

pipeline = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("model", model),
])

cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
scores = cross_validate(
    pipeline,
    X,
    y,
    cv=cv,
    scoring={"roc_auc": "roc_auc", "accuracy": "accuracy", "f1": "f1"},
    n_jobs=1,
    return_train_score=False,
)

metric_rows = []
for metric in ["test_roc_auc", "test_accuracy", "test_f1"]:
    vals = scores[metric]
    metric_rows.append({
        "metric": metric.replace("test_", ""),
        "mean": float(np.mean(vals)),
        "std": float(np.std(vals, ddof=1)),
        "n_folds": int(len(vals)),
    })
pd.DataFrame(metric_rows).to_csv(TABLES / "phase2_xgboost_cv_metrics.csv", index=False)

imputer = SimpleImputer(strategy="median")
X_imp = pd.DataFrame(imputer.fit_transform(X), columns=FEATURES, index=X.index)
model.fit(X_imp, y)

explainer = shap.TreeExplainer(model)
shap_values = explainer.shap_values(X_imp)
if isinstance(shap_values, list):
    shap_values = shap_values[-1]
shap_values = np.asarray(shap_values)
if shap_values.ndim == 3:
    shap_values = shap_values[:, :, -1]

importance = pd.DataFrame({
    "feature": FEATURES,
    "mean_abs_shap": np.abs(shap_values).mean(axis=0),
    "xgboost_gain_importance": model.feature_importances_,
}).sort_values("mean_abs_shap", ascending=False)
importance.to_csv(TABLES / "phase2_xgboost_shap_importance.csv", index=False)

plot_df = importance.sort_values("mean_abs_shap", ascending=True)
fig, ax = plt.subplots(figsize=(8, 5.8))
ax.barh(plot_df["feature"], plot_df["mean_abs_shap"])
ax.set_xlabel("Mean absolute SHAP value")
ax.set_ylabel("")
ax.set_title("XGBoost: CBDC advanced-stage feature importance")
fig.tight_layout()
fig.savefig(FIGURES / "phase2_xgboost_shap_importance.png", dpi=300, bbox_inches="tight")
plt.close(fig)

summary = {
    "n": int(len(model_df)),
    "positive_class_n": int(y.sum()),
    "negative_class_n": int((1 - y).sum()),
    "features": FEATURES,
    "cv": {row["metric"]: {"mean": row["mean"], "std": row["std"]} for row in metric_rows},
    "top_shap_features": importance.head(5)[["feature", "mean_abs_shap"]].to_dict("records"),
}
(ROOT / "outputs" / "phase2_xgboost_summary.json").write_text(
    json.dumps(summary, indent=2), encoding="utf-8"
)
print("XGBoost + SHAP analysis completed.")
