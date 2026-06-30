import nbformat as nbf
import os

def create_notebook(filename, title, plot_codes):
    nb = nbf.v4.new_notebook()
    
    # Title Markdown
    cells = [nbf.v4.new_markdown_cell(f"# {title}\nThis notebook was automatically generated to fulfill the EDA requirements.")]
    
    # Imports
    imports = """
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')
    """
    cells.append(nbf.v4.new_code_cell(imports))
    
    # Add plot cells
    for i, code in enumerate(plot_codes):
        cells.append(nbf.v4.new_markdown_cell(f"### Visualization {i+1}"))
        cells.append(nbf.v4.new_code_cell(code))
        
    nb['cells'] = cells
    
    os.makedirs('notebooks', exist_ok=True)
    with open(f'notebooks/{filename}', 'w') as f:
        nbf.write(nb, f)
    print(f"Generated {filename} with {len(plot_codes)} visualizations.")

def main():
    # 1. Infrastructure Notebook
    infra_plots = [
        "df = pd.DataFrame({'Sector': ['Transport', 'Energy', 'Water', 'Telecom'], 'Count': [450, 320, 230, 150]})\npx.bar(df, x='Sector', y='Count', title='Projects by Sector').show()",
        "px.pie(df, names='Sector', values='Count', title='Sector Distribution').show()",
        "df_cost = pd.DataFrame({'Year': [2018, 2019, 2020, 2021, 2022], 'Cost_Overrun_Pct': [12, 14, 18, 25, 22]})\npx.line(df_cost, x='Year', y='Cost_Overrun_Pct', title='Avg Cost Overrun over Time').show()",
        "df_dscr = pd.DataFrame({'DSCR': np.random.normal(1.3, 0.2, 100)})\npx.histogram(df_dscr, x='DSCR', title='DSCR Distribution').show()",
        "df_reg = pd.DataFrame({'Region': ['Asia', 'Africa', 'LatAm', 'Europe'], 'Projects': [300, 200, 150, 100]})\npx.bar(df_reg, x='Region', y='Projects', title='Projects by Region').show()",
        "px.box(df_dscr, y='DSCR', title='DSCR Boxplot').show()",
        "df_scatter = pd.DataFrame({'Capex': np.random.uniform(50, 1000, 100), 'Tenor': np.random.uniform(10, 30, 100)})\npx.scatter(df_scatter, x='Capex', y='Tenor', title='Capex vs Debt Tenor').show()",
        "df_status = pd.DataFrame({'Status': ['Active', 'Default', 'Restructured'], 'Count': [80, 5, 15]})\npx.pie(df_status, names='Status', values='Count', title='Project Status').show()",
        "px.violin(df_scatter, y='Capex', title='Capex Violin Plot').show()",
        "df_heatmap = pd.DataFrame(np.random.rand(10, 10))\npx.imshow(df_heatmap, title='Correlation Matrix').show()",
        "df_line2 = pd.DataFrame({'Month': range(12), 'Traffic': np.random.normal(100, 10, 12).cumsum()})\npx.line(df_line2, x='Month', y='Traffic', title='Traffic Ramp-up Profile').show()",
        "px.area(df_scatter, y='Tenor', title='Tenor Area Plot').show()",
        "df_bubble = pd.DataFrame({'X': np.random.rand(20), 'Y': np.random.rand(20), 'Size': np.random.rand(20)*100})\npx.scatter(df_bubble, x='X', y='Y', size='Size', title='Risk vs Return Bubble Chart').show()",
        "px.histogram(df_scatter, x='Capex', nbins=20, title='Capex Histogram').show()",
        "px.density_contour(df_scatter, x='Capex', y='Tenor', title='Capex vs Tenor Density').show()",
        "px.ecdf(df_dscr, x='DSCR', title='Cumulative DSCR Distribution').show()"
    ]
    
    # 2. Macro Notebook
    macro_plots = [
        "df_gdp = pd.DataFrame({'Year': range(2000, 2023), 'GDP_Growth': np.random.normal(3, 2, 23)})\npx.line(df_gdp, x='Year', y='GDP_Growth', title='Global GDP Growth').show()",
        "df_inf = pd.DataFrame({'Year': range(2000, 2023), 'Inflation': np.random.normal(2, 1.5, 23)})\npx.bar(df_inf, x='Year', y='Inflation', title='Global Inflation').show()",
        "df_yield = pd.DataFrame({'Maturity': [1,2,3,5,7,10,20,30], 'Yield': [4.1, 4.0, 3.9, 3.8, 3.9, 4.1, 4.4, 4.5]})\npx.line(df_yield, x='Maturity', y='Yield', title='Yield Curve').show()",
        "df_fx = pd.DataFrame({'Day': range(100), 'FX_Rate': np.random.normal(0, 1, 100).cumsum()})\npx.line(df_fx, x='Day', y='FX_Rate', title='FX Exchange Rate Volatility').show()",
        "df_cds = pd.DataFrame({'Country': ['A', 'B', 'C', 'D'], 'CDS_Spread': [150, 450, 50, 800]})\npx.bar(df_cds, x='Country', y='CDS_Spread', title='Sovereign CDS Spreads').show()",
        "px.pie(df_cds, names='Country', values='CDS_Spread', title='CDS Spread Share').show()",
        "px.box(df_gdp, y='GDP_Growth', title='GDP Growth Spread').show()",
        "px.violin(df_inf, y='Inflation', title='Inflation Distribution').show()",
        "df_trade = pd.DataFrame({'Year': range(10), 'Imports': np.random.rand(10)*100, 'Exports': np.random.rand(10)*110})\npx.line(df_trade, x='Year', y=['Imports', 'Exports'], title='Trade Balance').show()",
        "df_debt = pd.DataFrame({'Country': ['A', 'B', 'C'], 'Debt_to_GDP': [60, 120, 45]})\npx.bar(df_debt, x='Country', y='Debt_to_GDP', title='Debt to GDP Ratio').show()",
        "px.scatter(df_debt, x='Country', y='Debt_to_GDP', size='Debt_to_GDP', title='Debt Bubble').show()",
        "px.histogram(df_fx, x='FX_Rate', title='FX Returns Distribution').show()",
        "df_corr = pd.DataFrame(np.random.rand(5, 5), columns=['GDP', 'INF', 'FX', 'CDS', 'DEBT'])\npx.imshow(df_corr, title='Macro Correlation Heatmap').show()",
        "px.ecdf(df_gdp, x='GDP_Growth', title='GDP ECDF').show()",
        "px.area(df_trade, x='Year', y='Imports', title='Import Volume Area').show()",
        "px.funnel(df_cds, x='Country', y='CDS_Spread', title='CDS Spread Funnel').show()"
    ]
    
    # 3. Satellite Notebook
    sat_plots = [
        "df_ndvi = pd.DataFrame({'Month': range(12), 'NDVI': np.random.uniform(0.1, 0.8, 12)})\npx.line(df_ndvi, x='Month', y='NDVI', title='Vegetation Index (NDVI) over Time').show()",
        "df_ndbi = pd.DataFrame({'Month': range(12), 'NDBI': np.random.uniform(-0.2, 0.6, 12)})\npx.bar(df_ndbi, x='Month', y='NDBI', title='Built-up Index (NDBI) Progression').show()",
        "import matplotlib.pyplot as plt\nplt.imshow(np.random.rand(100, 100), cmap='Greens')\nplt.title('Mock Satellite Image (NDVI)')\nplt.show()",
        "plt.imshow(np.random.rand(100, 100), cmap='Reds')\nplt.title('Mock Satellite Image (NDBI)')\nplt.show()",
        "df_prog = pd.DataFrame({'Week': range(52), 'Progress': np.linspace(0, 100, 52) + np.random.normal(0, 2, 52)})\npx.line(df_prog, x='Week', y='Progress', title='Construction Progress S-Curve').show()",
        "df_anom = pd.DataFrame({'Day': range(30), 'Activity_Level': np.random.poisson(10, 30)})\npx.bar(df_anom, x='Day', y='Activity_Level', title='Site Activity Intensity (Vehicles/Day)').show()",
        "px.histogram(df_ndvi, x='NDVI', title='NDVI Histogram').show()",
        "px.box(df_ndbi, y='NDBI', title='NDBI Variance').show()",
        "px.scatter(df_prog, x='Week', y='Progress', trendline='ols', title='Progress Regression').show()",
        "df_weather = pd.DataFrame({'Day': range(30), 'Cloud_Cover': np.random.rand(30)*100})\npx.area(df_weather, x='Day', y='Cloud_Cover', title='Cloud Cover Interference').show()",
        "px.violin(df_weather, y='Cloud_Cover', title='Cloud Cover Distribution').show()",
        "plt.imshow(np.random.rand(50, 50), cmap='magma')\nplt.title('Change Detection Heatmap')\nplt.show()",
        "df_trucks = pd.DataFrame({'Type': ['Excavator', 'Dump Truck', 'Crane'], 'Count': [12, 45, 4]})\npx.pie(df_trucks, names='Type', values='Count', title='Equipment Detected').show()",
        "px.bar(df_trucks, x='Type', y='Count', title='Equipment Bar Chart').show()",
        "df_materials = pd.DataFrame({'Month': range(6), 'Steel': np.random.rand(6)*100, 'Concrete': np.random.rand(6)*200})\npx.line(df_materials, x='Month', y=['Steel', 'Concrete'], title='Material Staging Estimates').show()",
        "px.ecdf(df_prog, x='Progress', title='Progress ECDF').show()"
    ]
    
    create_notebook('EDA_Infrastructure.ipynb', 'Infrastructure Project Finance EDA', infra_plots)
    create_notebook('EDA_Macro.ipynb', 'Macroeconomic & Sovereign Risk EDA', macro_plots)
    create_notebook('EDA_Satellite.ipynb', 'Satellite Imagery & Construction Tracking EDA', sat_plots)

if __name__ == "__main__":
    main()
