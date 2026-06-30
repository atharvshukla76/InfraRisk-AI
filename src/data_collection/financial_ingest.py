import pandas as pd
import yfinance as yf
import QuantLib as ql
import datetime
import numpy as np

def fetch_interest_rates(start_date: str, end_date: str):
    """
    Fetches reference interest rates (e.g., SOFR/LIBOR proxies) using yfinance.
    For SOFR, we might use a proxy ETF or specific Treasury yields.
    """
    # Proxies for short term rates (e.g., 3-month Treasury bill)
    tickers = {'US_3M': '^IRX', 'US_6M': '^FVX'}
    try:
        data = yf.download(list(tickers.values()), start=start_date, end=end_date)
        df = data['Close'].reset_index()
        # Rename columns to our keys
        rename_map = {ticker: name for name, ticker in tickers.items()}
        df.rename(columns=rename_map, inplace=True)
        return df
    except Exception as e:
        print(f"Error fetching interest rates: {e}")
        return pd.DataFrame()

def fetch_credit_spreads(sector: str, start_date: str, end_date: str):
    """
    Fetches proxy credit spreads for infrastructure sectors.
    Uses Corporate Bond ETF yields minus Treasury yields as a proxy.
    """
    # Proxies: LQD (Investment Grade Corp), HYG (High Yield)
    tickers = {'IG_Corp': 'LQD', 'HY_Corp': 'HYG', 'Treasury_10Y': '^TNX'}
    try:
        data = yf.download(list(tickers.values()), start=start_date, end=end_date)
        df = data['Close'].reset_index()
        
        # Calculate a proxy spread (simplistic example)
        # Note: LQD is price, we'd need yield. For a real implementation, 
        # FRED API (via pandas-datareader) is much better for spreads (e.g., BAMLC0A0CM)
        print("Note: Use FRED API for accurate credit spreads in production.")
        return df
    except Exception as e:
        print(f"Error fetching credit spreads: {e}")
        return pd.DataFrame()

def fetch_project_finance_deals():
    """
    Loads historical project finance deal data (e.g., from a proprietary CSV or database).
    This dataset typically includes: ProjectID, Sector, Country, DebtAmount, EquityAmount,
    Tenor, BaseRate, Margin, DSCR_Base, DefaultFlag.
    """
    # Placeholder for loading proprietary data
    # return pd.read_csv('data/raw/financial/historical_deals.csv')
    print("Loading proprietary project finance deals (Placeholder)")
    
    # Generate some synthetic data for demonstration
    np.random.seed(42)
    data = {
        'deal_id': [f'PF_{i}' for i in range(100)],
        'sector': np.random.choice(['Transport', 'Energy', 'Telecom', 'Water'], 100),
        'country': np.random.choice(['USA', 'IND', 'BRA', 'ZAF'], 100),
        'debt_amount_m': np.random.uniform(50, 1000, 100),
        'tenor_years': np.random.randint(5, 30, 100),
        'margin_bps': np.random.uniform(150, 600, 100),
        'default_flag': np.random.binomial(1, 0.05, 100)
    }
    return pd.DataFrame(data)

def build_yield_curve(calc_date_str: str, rates_dict: dict):
    """
    Constructs a QuantLib yield curve for discounting cash flows.
    calc_date_str: 'YYYY-MM-DD'
    rates_dict: {tenor_months: rate_decimal}, e.g., {3: 0.05, 6: 0.051, 12: 0.052, 120: 0.055}
    """
    calc_date = ql.DateParser.parseFormatted(calc_date_str, '%Y-%m-%d')
    ql.Settings.instance().evaluationDate = calc_date
    
    helpers = []
    for months, rate in rates_dict.items():
        tenor = ql.Period(months, ql.Months)
        # Assuming these are simple swap/deposit rates for simplicity
        helpers.append(ql.DepositRateHelper(ql.QuoteHandle(ql.SimpleQuote(rate)),
                                            tenor,
                                            0, # settlement days
                                            ql.NullCalendar(),
                                            ql.ModifiedFollowing,
                                            False,
                                            ql.Actual360()))
                                            
    curve = ql.PiecewiseLogLinearDiscount(0, ql.NullCalendar(), helpers, ql.Actual360())
    return curve

if __name__ == "__main__":
    # curve = build_yield_curve('2023-01-01', {3: 0.04, 6: 0.045, 12: 0.048, 60: 0.042, 120: 0.045})
    # print("Discount factor at 5 years:", curve.discount(5.0))
    pass
