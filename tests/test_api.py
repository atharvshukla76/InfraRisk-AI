from fastapi.testclient import TestClient
from src.api.main import app
import pytest

client = TestClient(app)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "version": "1.0.0"}

def test_predict_composite_risk_valid():
    payload = {
        "project_id": "TEST-001",
        "sector": "Energy",
        "region": "North America",
        "debt_equity_ratio": 80.0,
        "dscr": 1.2,
        "historical_traffic_variance": 0.1,
        "asset_age_years": 10,
        "environmental_stress_idx": 0.4,
        "supply_chain_dependencies": 5
    }
    
    response = client.post("/api/v1/predict/composite", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert data["project_id"] == "TEST-001"
    assert "composite_score" in data
    assert "rating" in data
    assert 0.0 <= data["composite_score"] <= 100.0

def test_predict_composite_risk_invalid_schema():
    # Missing required fields like 'dscr'
    payload = {
        "project_id": "TEST-002",
        "sector": "Energy"
    }
    response = client.post("/api/v1/predict/composite", json=payload)
    assert response.status_code == 422 # FastAPI Unprocessable Entity for schema validation failure
