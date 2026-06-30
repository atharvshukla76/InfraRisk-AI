import pandas as pd
import numpy as np
import os

def load_project_schedule(project_id: str):
    """
    Loads the Work Breakdown Structure (WBS) schedule for a project.
    Expected to return a dataframe with columns:
    ActivityID, ActivityName, PlannedStart, PlannedEnd, ActualStart, ActualEnd, %Complete
    """
    file_path = f"data/raw/construction/schedules/{project_id}_schedule.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"Schedule file not found for {project_id}. Returning empty DataFrame.")
        return pd.DataFrame()

def load_cost_data(project_id: str):
    """
    Loads cost data (budgeted vs actual) for a project.
    Expected columns: ActivityID, BudgetedCost (BCWS), ActualCost (ACWP), EarnedValue (BCWP)
    """
    file_path = f"data/raw/construction/costs/{project_id}_costs.csv"
    if os.path.exists(file_path):
        return pd.read_csv(file_path)
    else:
        print(f"Cost file not found for {project_id}. Returning empty DataFrame.")
        return pd.DataFrame()

def generate_synthetic_construction_data(n_projects: int, output_dir: str = "data/raw/construction"):
    """
    Generates synthetic but realistic construction telemetry for training models.
    Creates schedule and cost CSVs for n_projects.
    """
    os.makedirs(f"{output_dir}/schedules", exist_ok=True)
    os.makedirs(f"{output_dir}/costs", exist_ok=True)
    
    np.random.seed(42)
    
    activities = ['Site Prep', 'Foundation', 'Superstructure', 'MEP', 'Finishing', 'Commissioning']
    
    for i in range(n_projects):
        project_id = f"PROJ_{i:03d}"
        
        # Base dates
        start_date = pd.Timestamp('2023-01-01') + pd.Timedelta(days=np.random.randint(0, 365))
        
        schedule_data = []
        cost_data = []
        
        current_date = start_date
        for idx, act in enumerate(activities):
            duration = np.random.randint(30, 120)
            planned_end = current_date + pd.Timedelta(days=duration)
            
            # Simulate actuals with some delays and cost overruns
            delay = int(np.random.normal(5, 15)) # mean 5 days delay
            actual_start = current_date + pd.Timedelta(days=max(0, delay//2))
            actual_end = planned_end + pd.Timedelta(days=delay)
            
            budget = np.random.uniform(1e6, 10e6)
            cost_overrun_pct = np.random.normal(0.05, 0.1) # 5% mean overrun
            actual_cost = budget * (1 + max(0, cost_overrun_pct))
            
            # Assuming project is 100% complete for historical training data
            pct_complete = 100 
            earned_value = budget # if 100% complete
            
            schedule_data.append({
                'ActivityID': f"A{idx+1}",
                'ActivityName': act,
                'PlannedStart': current_date.strftime('%Y-%m-%d'),
                'PlannedEnd': planned_end.strftime('%Y-%m-%d'),
                'ActualStart': actual_start.strftime('%Y-%m-%d'),
                'ActualEnd': actual_end.strftime('%Y-%m-%d'),
                'PctComplete': pct_complete
            })
            
            cost_data.append({
                'ActivityID': f"A{idx+1}",
                'BudgetedCost': budget,
                'ActualCost': actual_cost,
                'EarnedValue': earned_value
            })
            
            current_date = planned_end # Sequential activities for simplicity
            
        pd.DataFrame(schedule_data).to_csv(f"{output_dir}/schedules/{project_id}_schedule.csv", index=False)
        pd.DataFrame(cost_data).to_csv(f"{output_dir}/costs/{project_id}_costs.csv", index=False)
        
    print(f"Generated synthetic construction data for {n_projects} projects in {output_dir}")

def load_material_prices(start_date: str, end_date: str):
    """
    Loads raw material price indices (Steel, Cement, Labour).
    In production, this might come from FRED (e.g., PCU327320327320 for Ready-mix concrete)
    or commodity exchanges.
    """
    print("Loading material price indices (Placeholder)")
    # Generate synthetic time series
    dates = pd.date_range(start=start_date, end=end_date, freq='M')
    np.random.seed(42)
    df = pd.DataFrame({
        'Date': dates,
        'Steel_Index': 100 + np.cumsum(np.random.normal(0.5, 2, len(dates))),
        'Cement_Index': 100 + np.cumsum(np.random.normal(0.2, 1, len(dates))),
        'Labour_Index': 100 + np.cumsum(np.random.normal(0.3, 0.5, len(dates)))
    })
    return df

if __name__ == "__main__":
    # generate_synthetic_construction_data(10)
    pass
