# InfraRisk AI: Project Alpha (Wind Farm, Morocco)
**Date:** June 2026  
**Analyst:** InfraRisk AI  
**Sector:** Energy - Renewable (Wind)  

## Executive Summary
Project Alpha is a 150MW onshore wind farm located in Morocco. The project seeks $120M in senior debt financing on a 15-year tenor. Our AI ensemble model flags this project as **Investment Grade (BBB-)**, with a predicted PD of 2.4% over the loan life.

## AI Risk Engine Assessment
- **Credit Risk (XGBoost):** PD = 2.4%. Primary risk drivers are the moderate Sovereign Risk of Morocco and the 80% leverage ratio.
- **Demand/Revenue Risk (TFT):** The Temporal Fusion Transformer predicts stable generation output, but highlights a P90/P50 variance of 18% due to inter-annual wind stochasticity.
- **Physical Degradation (PINN):** The PINN model predicts turbine blade fatigue will reach critical thresholds in Year 12, recommending a robust MRA (Maintenance Reserve Account) build-up starting in Year 8.

## SHAP Explainability Analysis
*Why did the AI score this project a BBB-?*
- **Positive Contributors:**
    - `Offtake Agreement:` Long-term PPA with ONEE (state utility) reduces revenue volatility (+1.5% rating uplift).
    - `Technology Maturity:` Standard 3MW turbines (Proven technology, +0.8% uplift).
- **Negative Contributors:**
    - `Sovereign Risk:` Morocco's sovereign rating cap limits the maximum achievable project rating (-2.1% drag).

## Counterfactual Mitigation Pathway
To achieve a solid **BBB+** rating, the AI simulator recommends the following structural changes:
1. Decrease leverage from 80% to 72% (improves DSCR from 1.25x to 1.40x).
2. Expand the DSRA (Debt Service Reserve Account) from 3 months to 6 months to buffer against wind drought years.
