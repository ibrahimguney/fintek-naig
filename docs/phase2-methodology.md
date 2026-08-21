# Phase 2 methodology

Phase 2 aligns Global Findex explanatory variables with 2021 World Development Indicators (WDI) and 2021 values from the World Bank Worldwide Governance Indicators (WGI) 2025 Revision. The CBDC outcome remains the BIS March 2024 project-stage score.

The main econometric design uses nested specifications: digital-finance predictors (M1), macro/digital controls (M2), and a composite governance index (M3). The six WGI dimensions are tested separately as robustness checks to reduce multicollinearity. Ordered Probit/Logit model the 0–3 stage outcome; a binary pilot/live indicator is assessed with HC3-robust logistic regression. XGBoost with repeated stratified cross-validation provides nonlinear predictive evidence, and SHAP is used for model interpretation.

All coefficients and prediction results are interpreted as cross-sectional associations, not causal effects.
