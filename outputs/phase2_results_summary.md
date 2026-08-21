# Phase 2 reproducible results summary

This file is generated from the analysis outputs. Interpret coefficients as associations, not causal effects.

## Ordered probit — full specification

- `log_adult_population`: standardized coefficient = 0.664, SE = 0.149, p < .001, n = 95.
- `internet_users_2021`: standardized coefficient = 0.699, SE = 0.293, p = 0.017, n = 95.
- `account_ownership_2021`: standardized coefficient = 0.547, SE = 0.271, p = 0.043, n = 95.
- `log_gdp_per_capita_ppp_2021`: standardized coefficient = -0.680, SE = 0.386, p = 0.078, n = 95.
- `inflation_2021`: standardized coefficient = 0.202, SE = 0.121, p = 0.094, n = 95.
- `domestic_credit_private_2021`: standardized coefficient = 0.209, SE = 0.162, p = 0.195, n = 95.
- `online_bill_payment_2021`: standardized coefficient = -0.250, SE = 0.249, p = 0.315, n = 95.
- `wgi_governance_index_2021`: standardized coefficient = 0.216, SE = 0.279, p = 0.438, n = 95.

## Binary logit robustness — pilot/live vs no/research

- `log_adult_population`: OR for a 1-SD increase = 4.242, p < .001, n = 95.
- `account_ownership_2021`: OR for a 1-SD increase = 4.057, p = 0.018, n = 95.
- `internet_users_2021`: OR for a 1-SD increase = 4.856, p = 0.069, n = 95.
- `domestic_credit_private_2021`: OR for a 1-SD increase = 1.476, p = 0.268, n = 95.
- `log_gdp_per_capita_ppp_2021`: OR for a 1-SD increase = 0.446, p = 0.402, n = 95.
- `online_bill_payment_2021`: OR for a 1-SD increase = 0.597, p = 0.408, n = 95.
- `wgi_governance_index_2021`: OR for a 1-SD increase = 0.641, p = 0.567, n = 95.
- `inflation_2021`: OR for a 1-SD increase = 0.943, p = 0.880, n = 95.

## XGBoost predictive performance

- roc_auc: 0.710 ± 0.090 across 15 folds.
- accuracy: 0.721 ± 0.072 across 15 folds.
- f1: 0.522 ± 0.136 across 15 folds.

## SHAP ranking

1. `log_adult_population` — mean |SHAP| = 0.8816
2. `internet_users_2021` — mean |SHAP| = 0.6421
3. `account_ownership_2021` — mean |SHAP| = 0.5086
4. `domestic_credit_private_2021` — mean |SHAP| = 0.3060
5. `inflation_2021` — mean |SHAP| = 0.2820
6. `urban_population_2021` — mean |SHAP| = 0.2216
7. `fdi_net_inflows_2021` — mean |SHAP| = 0.2156

## WGI dimension robustness

- `wgi_government_effectiveness_2021`: coefficient = 0.541, p = 0.072, n = 95.
- `wgi_regulatory_quality_2021`: coefficient = 0.473, p = 0.113, n = 95.
- `wgi_political_stability_2021`: coefficient = -0.285, p = 0.185, n = 95.
- `wgi_control_corruption_2021`: coefficient = 0.281, p = 0.249, n = 95.
- `wgi_rule_of_law_2021`: coefficient = 0.198, p = 0.442, n = 95.
- `wgi_voice_accountability_2021`: coefficient = 0.045, p = 0.817, n = 95.
