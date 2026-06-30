import pytest
from src.risk_engine.composite_score import RiskAggregator

def test_risk_aggregator_weights():
    agg = RiskAggregator()
    # Ensure weights sum to 1.0 (100%)
    total_weight = sum(agg.weights.values())
    assert abs(total_weight - 1.0) < 1e-6, "Weights must sum to 1.0"

def test_composite_score_calculation():
    agg = RiskAggregator()
    
    # Test 1: Perfect project (0 risk everywhere)
    res = agg.calculate_composite_score(pd_val=0.0, demand_volatility=0.0, degradation_idx=0.0, contagion_prob=0.0)
    assert res['composite_score'] == 100.0
    assert res['rating'] == "AAA"
    
    # Test 2: Terrible project (Max risk everywhere)
    res2 = agg.calculate_composite_score(pd_val=1.0, demand_volatility=1.0, degradation_idx=1.0, contagion_prob=1.0)
    assert res2['composite_score'] == 0.0
    assert res2['rating'] == "D"
    
    # Test 3: Mixed project
    res3 = agg.calculate_composite_score(pd_val=0.1, demand_volatility=0.5, degradation_idx=0.2, contagion_prob=0.0)
    # Weighted risk = (0.1*0.4) + (0.5*0.25) + (0.2*0.2) + (0) = 0.04 + 0.125 + 0.04 = 0.205
    # Score = (1 - 0.205) * 100 = 79.5
    assert 79.0 <= res3['composite_score'] <= 80.0
    assert res3['rating'] == "A"
