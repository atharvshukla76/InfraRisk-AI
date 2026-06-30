import wbdata
import pandas as pd 
import datetime

def fetch_world_bank_macro(country_code: str, start_year: int, end_year: int):
    """Fetches GDP and Inflation data from the World Bank."""
    indicators = {
        "NY.GDP.MKTP.KD.ZG" : "GDP_Growth",
        "FP.CPI.TOTL.ZG": "Inflation"
    }
    start = datetime.datetime(start_year, 1, 1)
    end = datetime.datetime(end_year, 1, 1)

    df = wbdata.get_dataframe(indicators, country = country_code, date = (start, end))
    df = df.reset_index()
    df.rename(columns={'Date' : 'Date'}, inplace = True)
    df['Date'] = pd.to_datetime(df['Date'])
    return df.sort_values('Date').reset_index(drop = True)
if __name__ == "__main__":
    print(fetch_world_bank_macro("IND", 2015, 2023))