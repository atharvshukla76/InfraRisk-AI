import pandas as pd
import numpy as np 
def compute_descr(cfads: pd.Series, debt_service: pd.Series):
    """
    Computes Debt Service Coverage Ratio (DSCR).
    CFADS = Cash Flow Available for Debt Service
    """
    dscr = cfads/ debt_service
    dscr = dscr.replace([np.inf, -np.inf], np.nan).fillna(0)
    return {
        'dscr_min': dscr.min(),
        'dscr_avg': dscr.mean(),
        'dscr_profile': dscr.tolist()
    }
def compute_llcr(cfads: pd.Series, discount_rate: float, outstanding_debt: float):
    """Computes Loan Life Coverage Ratio (LLCR)."""
    periods = np.arange(1, len(cfads) + 1)
    discount_factors = (1 + discount_rate) ** periods
    npv_cfads = np.sum(cfads / discount_factors)
    return npv_cfads / outstanding_debt if  outstanding_debt > 0 else 0