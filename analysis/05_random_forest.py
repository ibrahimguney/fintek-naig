import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance
from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
from common import ROOT, PROCESSED, TABLES

DATA = PROCESSED / "cbdc_findex_merged_2021.csv"
df = pd.read_csv(DATA)
features = [
    "account_ownership_2021", "online_bill_payment_2021",
    "borrowed_any_2021", "log_adult_population",
]
rfdf = df[["advanced_cbdc", *features]].dropna().copy()
X = rfdf[features]
y = rfdf["advanced_cbdc"]

rf = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced_subsample",
    min_samples_leaf=3,
    max_features="sqrt",
    n_jobs=1,
)
cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=3, random_state=42)
scores = cross_validate(
    rf, X, y, cv=cv,
    scoring={"roc_auc": "roc_auc", "balanced_accuracy": "balanced_accuracy", "accuracy": "accuracy"},
    n_jobs=1,
)
metrics = []
for key in ["test_roc_auc", "test_balanced_accuracy", "test_accuracy"]:
    values = scores[key]
    metrics.append({
        "metric": key.replace("test_", ""),
        "mean": float(np.mean(values)),
        "sd": float(np.std(values)),
        "n_folds": len(values),
    })
pd.DataFrame(metrics).to_csv(TABLES / "table4_random_forest_cv_metrics.csv", index=False)

rf.fit(X, y)
perm = permutation_importance(rf, X, y, n_repeats=20, random_state=42, scoring="roc_auc")
importance = pd.DataFrame({
    "feature": X.columns,
    "importance_mean": perm.importances_mean,
    "importance_sd": perm.importances_std,
}).sort_values("importance_mean", ascending=False)
importance.to_csv(TABLES / "table5_random_forest_permutation_importance.csv", index=False)

summary = {
    "n": int(len(rfdf)),
    "roc_auc_mean": float(np.mean(scores["test_roc_auc"])),
    "roc_auc_sd": float(np.std(scores["test_roc_auc"])),
    "balanced_accuracy_mean": float(np.mean(scores["test_balanced_accuracy"])),
    "accuracy_mean": float(np.mean(scores["test_accuracy"])),
}
(ROOT / "outputs" / "random_forest_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
print("Random Forest completed.")
