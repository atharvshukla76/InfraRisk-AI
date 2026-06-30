# InfraRisk AI: Project Beta (Container Port, Ghana)
**Date:** June 2026  
**Analyst:** InfraRisk AI  
**Sector:** Transport - Ports & Maritime  

## Executive Summary
Project Beta is a major container port expansion in Tema, Ghana. The project requires $400M in debt financing. Our AI ensemble model flags this project as **High Risk (B)**, with a predicted PD of 7.8% over the loan life.

## AI Risk Engine Assessment
- **Credit Risk (XGBoost):** PD = 7.8%. The primary drivers are high sovereign risk (Ghana rating: B-/Caa1) and moderate demand risk tied to global trade volumes.
- **Demand/Revenue Risk (TFT):** The TFT model indicates high sensitivity to Chinese economic output and cocoa/gold export volumes.
- **Contagion Risk (GNN):** The Graph Neural Network detects a 15% portfolio concentration risk, as the project shares the same EPC contractor as two other distressed African port projects.

## SHAP Explainability Analysis
*Why did the AI score this project a B?*
- **Positive Contributors:**
    - `Sponsor Quality:` Backed by a Tier 1 global port operator (+1.2% uplift).
- **Negative Contributors:**
    - `Sovereign Risk:` Severe penalty due to high sovereign debt-to-GDP and historical FX volatility in Ghana (-4.5% drag).
    - `Demand Risk:` Pure volume risk (no minimum throughput guarantee from the government) (-1.8% drag).

## Counterfactual Mitigation Pathway
To achieve an acceptable **BB-** rating for our fund, the AI simulator recommends the following structural changes:
1. Secure a World Bank MIGA guarantee covering transfer and convertibility risk.
2. Negotiate a minimum throughput guarantee from the Ghana Port Authority for 70% of design capacity.
3. Introduce a 50% cash sweep mechanism during the first 5 years of operations to accelerate deleveraging.
