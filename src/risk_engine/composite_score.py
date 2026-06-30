class RiskAggregator:
    """
    Aggregates the raw outputs from various AI models (XGBoost, TFT, PINN, GNN)
    into a unified Composite Risk Score (0-100) and assigns a Credit Rating.
    """
    
    def __init__(self):
        # Default Weights for Infrastructure Project Finance
        self.weights = {
            'credit_risk': 0.40,   # XGBoost PD
            'demand_risk': 0.25,   # TFT Quantile Spread
            'structural_risk': 0.20, # PINN Degradation Index
            'contagion_risk': 0.15   # GNN Failure Probability
        }
        
    def calculate_composite_score(self, pd_val: float, demand_volatility: float, 
                                  degradation_idx: float, contagion_prob: float) -> dict:
        """
        Calculates the composite risk score. All inputs should be normalized roughly between 0.0 and 1.0,
        where 1.0 represents maximum risk.
        
        Returns:
            dict: { 'composite_score': float, 'rating': str, 'details': dict }
        """
        # Ensure inputs are clamped
        pd_val = max(0.0, min(1.0, pd_val))
        demand_volatility = max(0.0, min(1.0, demand_volatility))
        degradation_idx = max(0.0, min(1.0, degradation_idx))
        contagion_prob = max(0.0, min(1.0, contagion_prob))
        
        # Calculate weighted risk (0.0 to 1.0)
        weighted_risk = (
            (pd_val * self.weights['credit_risk']) +
            (demand_volatility * self.weights['demand_risk']) +
            (degradation_idx * self.weights['structural_risk']) +
            (contagion_prob * self.weights['contagion_risk'])
        )
        
        # Convert to a 0-100 Score (where 100 is PERFECT, i.e., Zero Risk)
        composite_score = (1.0 - weighted_risk) * 100.0
        
        # Determine Rating based on score
        rating = self._determine_rating(composite_score)
        
        return {
            'composite_score': round(composite_score, 2),
            'rating': rating,
            'breakdown': {
                'credit_risk_contribution': round(pd_val * self.weights['credit_risk'] * 100, 2),
                'demand_risk_contribution': round(demand_volatility * self.weights['demand_risk'] * 100, 2),
                'structural_risk_contribution': round(degradation_idx * self.weights['structural_risk'] * 100, 2),
                'contagion_risk_contribution': round(contagion_prob * self.weights['contagion_risk'] * 100, 2)
            }
        }
        
    def _determine_rating(self, score: float) -> str:
        if score >= 90: return "AAA"
        if score >= 80: return "AA"
        if score >= 70: return "A"
        if score >= 60: return "BBB"
        if score >= 50: return "BB"
        if score >= 40: return "B"
        if score >= 20: return "CCC"
        return "D"

if __name__ == "__main__":
    agg = RiskAggregator()
    res = agg.calculate_composite_score(pd_val=0.05, demand_volatility=0.2, degradation_idx=0.1, contagion_prob=0.01)
    print("Test Score:", res)
