from pydantic import BaseModel, Field
from typing import Optional

class ProjectInferenceRequest(BaseModel):
    """
    Schema for submitting a project to the Composite Risk Engine.
    Requires baseline metrics that the internal models will use for inference.
    """
    project_id: str = Field(..., example="PRJ-1044")
    sector: str = Field(..., example="Transport")
    region: str = Field(..., example="Europe")
    
    # Financial Inputs (Used by XGBoost)
    debt_equity_ratio: float = Field(..., ge=0, example=75.0)
    dscr: float = Field(..., ge=0, example=1.4, description="Debt Service Coverage Ratio")
    
    # Demand Inputs (Used by TFT)
    historical_traffic_variance: float = Field(..., example=0.15)
    
    # Physical Inputs (Used by PINN)
    asset_age_years: int = Field(..., ge=0, example=5)
    environmental_stress_idx: float = Field(..., ge=0.0, le=1.0, example=0.6)
    
    # Network Inputs (Used by GNN)
    supply_chain_dependencies: int = Field(..., ge=0, example=12)

class RiskInferenceResponse(BaseModel):
    """
    Schema for the response returning the Composite Risk Score and Rating.
    """
    project_id: str
    composite_score: float = Field(..., ge=0.0, le=100.0)
    rating: str
    breakdown: dict
    status: str = "Success"
