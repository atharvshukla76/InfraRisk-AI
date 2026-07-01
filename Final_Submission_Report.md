# Final Internship Submission Report
**Zetheta Algorithms Private Limited – Data Scientist Internship**

**Project Name:** InfraRisk AI (MatRisk AI v1.0)
**Date:** June 30, 2026

---

## 1. Executive Summary
InfraRisk AI is a comprehensive, enterprise-grade project finance and risk intelligence platform built for modern infrastructure underwriting. The system successfully merges traditional financial metrics (such as DSCR and PD) with advanced Machine Learning frameworks, spanning from raw data ingestion to gamified simulations.

### Key Deliverables Achieved
- **Fully Functional AI Risk Engine:** Integrates multiple state-of-the-art architectures.
- **Royal-Themed Interactive Dashboard:** Deployed and fully operational.
- **Gamified Simulation Mode:** Allows users to simulate 30-year infrastructure portfolio risks against macroeconomic shocks.
- **Containerized Architecture:** Production-ready via Docker and automated CI/CD pipelines.

---

## 2. Important Links
- **GitHub Repository (Transferred):** [https://github.com/atharvshukla76/InfraRisk-AI](https://github.com/atharvshukla76/InfraRisk-AI)
- **Live Streamlit Dashboard:** [https://infrarisk-ai-jdbn7hyqjfybclfjskqsha.streamlit.app/](https://infrarisk-ai-jdbn7hyqjfybclfjskqsha.streamlit.app/)
- **15-Minute Video Demonstration:** [Watch on Google Drive](https://drive.google.com/file/d/1YfaNDBmvK62KfzHEVDyODHBJv0F77yLo/view?usp=sharing)

---

## 3. Machine Learning Architecture
The core intelligence of InfraRisk AI is built on four distinct pillars of machine learning:

1. **Credit Risk & Underwriting (XGBoost):**
   Predicts the Probability of Default (PD) and projects Debt Service Coverage Ratios (DSCR) using historical traffic volatility, macroeconomic indicators, and financial structuring constraints.

2. **Demand Forecasting (Temporal Fusion Transformers):**
   Utilizes PyTorch-based TFTs to project long-term toll revenue and energy utilization, adjusting for historical analogs and seasonal patterns.

3. **Physical Asset Degradation (Physics-Informed Neural Networks - PINNs):**
   Models physical wear and tear on infrastructure (e.g., bridge fatigue, concrete spalling) by integrating real-world physics differential equations into neural network loss functions.

4. **Spatial Contagion Risk (Graph Neural Networks - GNNs):**
   Maps interdependencies across European highway networks and energy grids. If a critical node (e.g., Paris Transport Hub) fails due to climate stress, the GNN calculates the cascading financial impact on the entire portfolio.

---

## 4. Software Engineering & Deployment
The system emphasizes robust software engineering principles for enterprise scalability:
- **FastAPI Backend:** Handles asynchronous model inference and routes.
- **Streamlit Frontend:** Built with a bespoke "Royal" CSS aesthetic.
- **Dockerization:** `docker-compose up --build` instantiates the entire architecture seamlessly.
- **Testing & CI/CD:** Integrated `pytest` suites automated through GitHub Actions for continuous integration.

---
*This report certifies the successful completion of the InfraRisk AI project as outlined in the Zetheta Data Scientist Internship Curriculum.*
