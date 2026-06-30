import random
import pandas as pd
import numpy as np

class InfraRiskSimulation:
    """
    Gamified Simulation Engine for InfraRisk AI.
    Allows users (investors) to manage an infrastructure portfolio across 30 years (turns),
    dealing with chaotic macro shocks, black swan events, and changing risk profiles.
    """
    def __init__(self, initial_budget=10000.0):
        self.turn = 1
        self.max_turns = 30
        self.budget = initial_budget
        self.portfolio = []
        self.macro_state = "Normal"
        self.history = []
        self.game_over = False

    def get_available_projects(self):
        """Generates random infrastructure deals available for investment."""
        projects = []
        sectors = ['Transport', 'Energy', 'Telecom', 'Water']
        regions = ['North America', 'Europe', 'Asia', 'Latin America', 'Africa']
        
        for _ in range(3):
            capex = round(random.uniform(500, 3000), 2)
            projects.append({
                "id": f"PRJ_{random.randint(1000, 9999)}",
                "sector": random.choice(sectors),
                "region": random.choice(regions),
                "capex": capex,
                "expected_irr": round(random.uniform(0.08, 0.18), 3),
                "risk_rating": random.choice(["AAA", "AA", "A", "BBB", "BB", "B", "CCC"])
            })
        return projects

    def invest(self, project: dict):
        """Invests the budget into a project."""
        if self.budget >= project['capex']:
            self.budget -= project['capex']
            project['status'] = "Active"
            project['current_value'] = project['capex']
            self.portfolio.append(project)
            return True, "Investment successful."
        return False, "Insufficient budget."

    def advance_turn(self):
        """Advances the simulation by one year."""
        if self.turn >= self.max_turns or self.budget < 0:
            self.game_over = True
            return self._summarize()

        self.turn += 1
        
        # 1. Generate Macro Shock
        shock = self._generate_macro_shock()
        
        # 2. Update Portfolio Performance
        total_revenue = 0
        for p in self.portfolio:
            # Base return
            annual_return = p['capex'] * p['expected_irr']
            
            # Apply shock multiplier based on sector/region
            multiplier = 1.0
            if shock['type'] == "Pandemic" and p['sector'] == "Transport":
                multiplier = 0.2  # Massive drop in traffic
            elif shock['type'] == "Energy Crisis" and p['sector'] == "Energy":
                multiplier = 2.0  # Huge windfall profits
            elif shock['type'] == "Interest Rate Hike":
                multiplier = 0.8  # Debt becomes expensive
                
            actual_revenue = annual_return * multiplier
            
            # Default risk check
            if multiplier < 0.5 and p['risk_rating'] in ["B", "CCC"]:
                if random.random() < 0.3: # 30% chance of default under severe stress
                    p['status'] = "Defaulted"
                    p['current_value'] = 0
                    actual_revenue = 0
                    
            if p['status'] == "Active":
                total_revenue += actual_revenue
                p['current_value'] *= (1 + (p['expected_irr'] * multiplier - 0.05)) # Asset appreciation/depreciation
                
        # 3. Update Budget
        self.budget += total_revenue
        
        # 4. Record history
        state = {
            "turn": self.turn,
            "budget": round(self.budget, 2),
            "macro_state": shock['name'],
            "active_assets": sum(1 for p in self.portfolio if p['status'] == 'Active'),
            "defaults": sum(1 for p in self.portfolio if p['status'] == 'Defaulted')
        }
        self.history.append(state)
        
        return state

    def _generate_macro_shock(self):
        """Generates random events (Black Swans)."""
        events = [
            {"name": "Stable Economic Growth", "type": "Normal", "prob": 0.6},
            {"name": "Global Pandemic", "type": "Pandemic", "prob": 0.05},
            {"name": "Severe Energy Crisis", "type": "Energy Crisis", "prob": 0.1},
            {"name": "Central Bank Rate Hike", "type": "Interest Rate Hike", "prob": 0.2},
            {"name": "Supply Chain Collapse", "type": "Supply Chain", "prob": 0.05}
        ]
        
        # Weighted random choice
        r = random.random()
        cumulative = 0.0
        for event in events:
            cumulative += event['prob']
            if r <= cumulative:
                self.macro_state = event['name']
                return event
        
        self.macro_state = events[0]['name']
        return events[0]

    def _summarize(self):
        """Returns end game stats."""
        total_asset_value = sum(p['current_value'] for p in self.portfolio)
        return {
            "status": "Game Over",
            "final_budget": round(self.budget, 2),
            "total_asset_value": round(total_asset_value, 2),
            "total_equity": round(self.budget + total_asset_value, 2)
        }

if __name__ == "__main__":
    game = InfraRiskSimulation()
    print("Initial Budget:", game.budget)
    deals = game.get_available_projects()
    game.invest(deals[0])
    
    for _ in range(5):
        res = game.advance_turn()
        print(res)