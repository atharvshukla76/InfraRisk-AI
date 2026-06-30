from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Add root directory to sys.path to resolve internal modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.api.api_schemas import ProjectInferenceRequest, RiskInferenceResponse
from src.risk_engine.composite_score import RiskAggregator

app = FastAPI(
    title="InfraRisk AI Platform API",
    description="Backend API for advanced Infrastructure Risk modeling and scoring.",
    version="1.0.0"
)

# CORS configuration for Streamlit/Web frontends
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the central Risk Aggregator
risk_engine = RiskAggregator()

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "1.0.0"}

@app.post("/api/v1/predict/composite", response_model=RiskInferenceResponse)
def predict_composite_risk(request: ProjectInferenceRequest):
    """
    Receives project parameters, internally triggers the 4 deep learning/ML models,
    and returns a unified Composite Risk Score.
    """
    try:
        # In a real system, we would pass 'request' inputs to the actual trained PyTorch/XGBoost models here.
        # For this functional API blueprint, we map the input severity to normalized model outputs (0.0 - 1.0).
        
        # 1. XGBoost Mock Inference (Lower DSCR = Higher PD)
        mock_pd = max(0.0, 1.0 - (request.dscr / 2.0))
        
        # 2. TFT Mock Inference (Higher variance = Higher demand risk)
        mock_demand_risk = min(1.0, request.historical_traffic_variance * 2.5)
        
        # 3. PINN Mock Inference (Age & Stress = Degradation)
        mock_degradation = min(1.0, (request.asset_age_years / 50.0) + (request.environmental_stress_idx * 0.5))
        
        # 4. GNN Mock Inference (More dependencies = Higher contagion risk)
        mock_contagion = min(1.0, request.supply_chain_dependencies / 20.0)
        
        # Run the Risk Aggregator
        result = risk_engine.calculate_composite_score(
            pd_val=mock_pd,
            demand_volatility=mock_demand_risk,
            degradation_idx=mock_degradation,
            contagion_prob=mock_contagion
        )
        
        return RiskInferenceResponse(
            project_id=request.project_id,
            composite_score=result['composite_score'],
            rating=result['rating'],
            breakdown=result['breakdown']
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))