import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

# -----------------------------------------
# Page Configuration
# -----------------------------------------
st.set_page_config(
    page_title="InfraRisk AI | Royal Dashboard",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------
# Load Royal CSS Theme
# -----------------------------------------
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), 'style.css')
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
            
            # Also inject Google Fonts for the royal aesthetic
            st.markdown("""
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700&display=swap');
            </style>
            """, unsafe_allow_html=True)

load_css()

# -----------------------------------------
# Sidebar
# -----------------------------------------
st.sidebar.title("🏛️ InfraRisk AI")
st.sidebar.markdown("---")
page = st.sidebar.radio("Navigate", 
    [
        "Portfolio Overview", 
        "Credit Risk & Pricing",
        "Geospatial & Climate Risk",
        "Macro & Sovereign Risk",
        "Gamified Simulation",
        "New Project Assessment", 
        "Macroeconomic Stress Test"
    ]
)
st.sidebar.markdown("---")
st.sidebar.info("Model Status: Online\n\nActive Nodes: 4\n\nData Sync: Optimal")

# -----------------------------------------
# Page: Portfolio Overview
# -----------------------------------------
if page == "Portfolio Overview":
    st.title("Imperial Portfolio Overview")
    st.markdown("Monitor the risk and performance of active infrastructure assets globally.")
    
    # Top-level metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total AUM ($B)", "42.5", "+1.2%")
    col2.metric("Avg Portfolio PD", "2.4%", "-0.3%")
    col3.metric("Critical Alerts", "3", "High Traffic")
    col4.metric("Avg DSCR", "1.45x", "Stable")
    
    st.markdown("---")
    
    # Map and Chart
    col_map, col_chart = st.columns([2, 1])
    
    with col_map:
        st.subheader("Asset Geo-Distribution")
        # Generate dummy geo data for map
        df_geo = pd.DataFrame({
            'lat': [40.71, 51.50, 35.68, 19.07, -23.55],
            'lon': [-74.00, -0.12, 139.69, 72.87, -46.63],
            'project': ['Hudson Rail', 'Thames Tunnel', 'Tokyo Grid', 'Mumbai Coastal', 'Sao Paulo Metro'],
            'risk': [0.01, 0.05, 0.02, 0.08, 0.12]
        })
        
        # Royal themed map using plotly
        fig_map = px.scatter_mapbox(df_geo, lat="lat", lon="lon", hover_name="project", hover_data=["risk"],
                        color="risk", color_continuous_scale=px.colors.sequential.YlOrRd, size_max=15, zoom=1)
        fig_map.update_layout(
            mapbox_style="carto-darkmatter",
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cfb53b', family='Cinzel')
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
    with col_chart:
        st.subheader("Sector Exposure")
        labels = ['Transport', 'Energy', 'Telecom', 'Water']
        values = [45, 30, 15, 10]
        # Golden pie chart
        fig_pie = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, 
                                         marker=dict(colors=['#cfb53b', '#a68b28', '#ffd700', '#8a6d1c']))])
        fig_pie.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cfb53b', family='Cinzel'),
            showlegend=False
        )
        st.plotly_chart(fig_pie, use_container_width=True)

# -----------------------------------------
# Page: New Project Assessment
# -----------------------------------------
elif page == "New Project Assessment":
    st.title("Project Underwriting")
    st.markdown("Run AI Credit Risk assessment (XGBoost PD Model) on a prospective asset.")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Financial Structuring")
        capex = st.number_input("CAPEX ($M)", min_value=10, max_value=10000, value=500)
        debt_ratio = st.slider("Debt Ratio (%)", 10, 90, 70)
        tenor = st.slider("Debt Tenor (Years)", 5, 40, 20)
        
        st.subheader("Macro Environment")
        gdp_growth = st.slider("Host Country GDP Growth (%)", -5.0, 10.0, 3.5)
        country_risk = st.slider("Sovereign Risk Score (1-10)", 1.0, 10.0, 4.0)
        
        analyze_btn = st.button("⚜️ Execute AI Assessment ⚜️")
        
    with col2:
        if analyze_btn:
            with st.spinner("Invoking XGBoost and PyTorch Models..."):
                # Mock Model Prediction Logic
                import time
                time.sleep(1.5) # simulate computation
                
                # Simple logic representing the ML model's output
                debt_amount = capex * (debt_ratio/100)
                risk_penalty = (country_risk / 10.0) * max(0, 5.0 - gdp_growth)
                pd = max(0.005, min(0.99, (debt_ratio / 100) * 0.05 + (risk_penalty * 0.02)))
                
                dscr_avg = 1.6 - (debt_ratio/100 * 0.5) - (risk_penalty * 0.1)
                
                st.subheader("Assessment Results")
                rcol1, rcol2, rcol3 = st.columns(3)
                rcol1.metric("Probability of Default (PD)", f"{pd:.2%}")
                rcol2.metric("Projected Avg DSCR", f"{dscr_avg:.2f}x")
                rcol3.metric("Credit Rating", "A-" if pd < 0.02 else "BBB" if pd < 0.05 else "BB+")
                
                st.markdown("### Projected Cash Flow Available for Debt Service (CFADS)")
                years = np.arange(1, tenor+1)
                cfads = capex * 0.12 * (1 + np.random.normal(0.02, 0.05, tenor).cumsum())
                debt_service = [debt_amount / tenor * 1.5] * tenor
                
                fig = go.Figure()
                fig.add_trace(go.Bar(x=years, y=cfads, name="CFADS", marker_color='#cfb53b'))
                fig.add_trace(go.Scatter(x=years, y=debt_service, name="Debt Service", mode='lines', line=dict(color='red', width=3)))
                fig.update_layout(
                    title="CFADS vs Debt Service Profile",
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='#cfb53b', family='Cinzel')
                )
                st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------
# Page: Gamified Simulation
# -----------------------------------------
elif page == "Gamified Simulation":
    st.title("🎲 Infrastructure Investor: The Simulation")
    st.markdown("Navigate macro shocks, build your portfolio, and survive 30 years of market volatility.")
    
    # Initialize game state in session_state if not exists
    if 'game' not in st.session_state:
        import sys
        sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        from src.simulation.game_engine import InfraRiskSimulation
        st.session_state.game = InfraRiskSimulation(initial_budget=5000.0)
        st.session_state.available_projects = st.session_state.game.get_available_projects()
        
    game = st.session_state.game
    
    if game.game_over:
        st.error("GAME OVER")
        st.json(game._summarize())
        if st.button("Restart Simulation"):
            del st.session_state.game
            st.experimental_rerun()
    else:
        # Top HUD
        col1, col2, col3 = st.columns(3)
        col1.metric("Turn (Year)", f"{game.turn} / {game.max_turns}")
        col2.metric("Treasury Budget", f"${game.budget:,.2f}M")
        col3.metric("Macro Environment", game.macro_state)
        
        st.markdown("---")
        
        # Actions
        col_act, col_port = st.columns([1, 1])
        
        with col_act:
            st.subheader("Market: Available Assets")
            for p in st.session_state.available_projects:
                with st.container():
                    st.markdown(f"**{p['id']} - {p['sector']} ({p['region']})**")
                    st.write(f"Cost: ${p['capex']}M | Expected IRR: {p['expected_irr']:.1%} | Risk: {p['risk_rating']}")
                    if st.button(f"Acquire {p['id']}", key=p['id']):
                        success, msg = game.invest(p)
                        if success:
                            st.success(msg)
                            st.session_state.available_projects.remove(p)
                        else:
                            st.error(msg)
            
            st.markdown("---")
            if st.button("⏩ Advance 1 Year", use_container_width=True):
                res = game.advance_turn()
                st.session_state.available_projects = game.get_available_projects() # Refresh market
                if res.get('macro_state') != "Stable Economic Growth":
                    st.warning(f"🚨 MACRO SHOCK: {res.get('macro_state')}!")
                
        with col_port:
            st.subheader("Your Portfolio")
            if not game.portfolio:
                st.info("No active investments. Acquire an asset to begin generating yield.")
            else:
                for p in game.portfolio:
                    color = "green" if p['status'] == "Active" else "red"
                    st.markdown(f"<span style='color:{color}'>**{p['id']}** ({p['sector']}) - Status: {p['status']}</span>", unsafe_allow_html=True)
                    st.write(f"Current Value: ${p.get('current_value', 0):,.2f}M")
                    st.markdown("---")

# -----------------------------------------
# Page: Credit Risk & Pricing (API Integration)
# -----------------------------------------
elif page == "Credit Risk & Pricing":
    st.title("⚖️ Credit Risk & Pricing Engine")
    st.markdown("Query the AI backend for real-time project risk assessment.")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.subheader("Project Parameters")
        with st.form("risk_form"):
            project_id = st.text_input("Project ID", "PRJ-9921")
            sector = st.selectbox("Sector", ["Transport", "Energy", "Water", "Telecom"])
            region = st.selectbox("Region", ["North America", "Europe", "Asia", "Latin America", "Africa"])
            dscr = st.slider("Debt Service Coverage Ratio (DSCR)", 0.5, 3.0, 1.4, 0.1)
            debt_ratio = st.slider("Debt/Equity Ratio (%)", 0, 100, 75)
            traffic_var = st.slider("Historical Demand Volatility", 0.0, 0.5, 0.15, 0.01)
            age = st.slider("Asset Age (Years)", 0, 100, 5)
            stress = st.slider("Environmental Stress Index", 0.0, 1.0, 0.6, 0.1)
            supply_chain = st.slider("Supply Chain Dependencies", 0, 50, 12)
            
            submitted = st.form_submit_button("Run AI Assessment")
            
    with col2:
        st.subheader("AI Prediction Results")
        if submitted:
            import requests
            # Payload matching the Pydantic schema
            payload = {
                "project_id": project_id,
                "sector": sector,
                "region": region,
                "debt_equity_ratio": float(debt_ratio),
                "dscr": float(dscr),
                "historical_traffic_variance": float(traffic_var),
                "asset_age_years": int(age),
                "environmental_stress_idx": float(stress),
                "supply_chain_dependencies": int(supply_chain)
            }
            
            with st.spinner("Querying FastAPI Backend..."):
                try:
                    response = requests.post("http://localhost:8000/api/v1/predict/composite", json=payload)
                    if response.status_code == 200:
                        data = response.json()
                        score = data["composite_score"]
                        rating = data["rating"]
                        
                        # Display beautiful metric
                        st.metric("Composite Risk Score (0-100)", f"{score:.1f}", f"Rating: {rating}", delta_color="off")
                        
                        # Plot gauge chart
                        import plotly.graph_objects as go
                        fig = go.Figure(go.Indicator(
                            mode = "gauge+number",
                            value = score,
                            title = {'text': "Project Viability"},
                            gauge = {
                                'axis': {'range': [None, 100]},
                                'bar': {'color': "darkblue"},
                                'steps': [
                                    {'range': [0, 40], 'color': "red"},
                                    {'range': [40, 70], 'color': "orange"},
                                    {'range': [70, 100], 'color': "green"}],
                            }
                        ))
                        fig.update_layout(height=300, margin=dict(l=10, r=10, t=40, b=10))
                        st.plotly_chart(fig, use_container_width=True)
                        
                        with st.expander("View Risk Breakdown"):
                            st.json(data["breakdown"])
                    else:
                        st.error(f"API Error: {response.status_code}")
                except Exception as e:
                    st.error(f"Failed to connect to API. Make sure uvicorn is running! Error: {e}")
        else:
            st.info("Adjust the parameters on the left and click 'Run AI Assessment' to query the Risk Engine.")

# -----------------------------------------
# Page: Geospatial & Climate Risk
# -----------------------------------------
elif page == "Geospatial & Climate Risk":
    st.title("🌍 Geospatial Asset Mapping")
    st.markdown("Visualize infrastructure assets and overlay climate stress models.")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("European Highway Network & Flood Risk")
        
        # Realistic coordinates for major European infrastructure hubs
        cities = ['Paris', 'London', 'Berlin', 'Madrid', 'Rome', 'Amsterdam', 'Brussels', 'Vienna', 'Munich', 'Prague', 'Warsaw', 'Budapest']
        lats = [48.8566, 51.5074, 52.5200, 40.4168, 41.9028, 52.3676, 50.8503, 48.2082, 48.1351, 50.0755, 52.2297, 47.4979]
        lons = [2.3522, -0.1278, 13.4050, -3.7038, 12.4964, 4.9041, 4.3517, 16.3738, 11.5820, 14.4378, 21.0122, 19.0402]
        
        # Simulate Climate/Flood Risk Scores (0 to 100)
        np.random.seed(42)
        flood_risk = np.random.randint(10, 95, size=len(cities))
        
        df_climate = pd.DataFrame({
            'Asset Hub': cities,
            'lat': lats,
            'lon': lons,
            'Flood Risk (RCP 8.5)': flood_risk
        })
        
        # Premium map visualization
        fig_map = px.scatter_mapbox(
            df_climate, 
            lat="lat", 
            lon="lon", 
            hover_name="Asset Hub", 
            hover_data=["Flood Risk (RCP 8.5)"],
            color="Flood Risk (RCP 8.5)", 
            color_continuous_scale=px.colors.sequential.Sunsetdark, 
            size="Flood Risk (RCP 8.5)",
            size_max=25, 
            zoom=3.5
        )
        fig_map.update_layout(
            mapbox_style="carto-darkmatter",
            margin={"r":0,"t":0,"l":0,"b":0},
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cfb53b', family='Cinzel')
        )
        st.plotly_chart(fig_map, use_container_width=True)
        
    with col2:
        st.subheader("Regional Vulnerability")
        st.dataframe(df_climate.sort_values(by='Flood Risk (RCP 8.5)', ascending=False).reset_index(drop=True), use_container_width=True)
        
        st.warning("🚨 Amsterdam Hub indicates critical sea-level rise vulnerability under IPCC RCP 8.5 scenario. 18% reduction in CA-RUL (Climate-Adjusted Remaining Useful Life).")
        
        st.info("In the full production environment, this module pulls live Sentinel-2 satellite imagery using Rasterio and generates real-time flood risk overlays using EarthEngine.")

# -----------------------------------------
# Page: Macro & Sovereign Risk
# -----------------------------------------
elif page == "Macro & Sovereign Risk":
    st.title("📈 Macro & Sovereign Yields")
    st.markdown("Live macroeconomic indicators and simulated yield curves.")
    
    st.subheader("Simulated 30-Year Bond Yield Curve")
    # Generate a mock yield curve
    maturities = [1, 2, 3, 5, 7, 10, 20, 30]
    yields = [4.5, 4.2, 4.0, 3.8, 3.9, 4.1, 4.3, 4.4]
    
    fig = px.line(x=maturities, y=yields, markers=True, 
                  labels={'x': 'Maturity (Years)', 'y': 'Yield (%)'},
                  title="Sovereign Debt Yield Curve (Mock)")
    fig.update_traces(line_color="#B8860B", marker=dict(size=8))
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------------------
# Page: Macroeconomic Stress Test
# -----------------------------------------
elif page == "Macroeconomic Stress Test":
    st.title("🌪️ Macroeconomic Stress Test")
    st.markdown("Simulate the impact of severe macroeconomic shocks on portfolio-wide Debt Service Coverage Ratios (DSCR).")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Shock Scenarios")
        st.selectbox("Select Historical Analogue", ["Asian Financial Crisis (1997)", "Global Financial Crisis (2008)", "COVID-19 Pandemic (2020)", "Custom Scenario"])
        gdp_shock = st.slider("GDP Contraction (%)", -15.0, 0.0, -5.5)
        rate_shock = st.slider("Interest Rate Spike (bps)", 0, 500, 250)
        fx_shock = st.slider("FX Depreciation (%)", 0, 50, 20)
        
        st.button("Run Monte Carlo Stress Test")
        
    with col2:
        st.subheader("DSCR Trajectory under Stress")
        years = np.arange(1, 11)
        base_dscr = np.array([1.45, 1.48, 1.50, 1.55, 1.60, 1.62, 1.65, 1.68, 1.70, 1.75])
        
        # Calculate stress impact based on sliders
        impact = (gdp_shock * 0.05) - (rate_shock * 0.001) - (fx_shock * 0.01)
        stress_dscr = base_dscr + impact
        # Add some recovery over time
        stress_dscr = stress_dscr + np.linspace(0, abs(impact)*0.8, 10)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=years, y=base_dscr, name="Base Case DSCR", mode='lines+markers', line=dict(color='#cfb53b', width=3)))
        fig.add_trace(go.Scatter(x=years, y=stress_dscr, name="Stressed DSCR", mode='lines+markers', line=dict(color='red', width=3, dash='dash')))
        
        # Add the 1.0x default threshold line
        fig.add_hline(y=1.0, line_dash="dot", line_color="orange", annotation_text="Default Threshold (1.0x)")
        
        fig.update_layout(
            title="Portfolio Average DSCR Projection",
            xaxis_title="Years Forward",
            yaxis_title="DSCR (x)",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#cfb53b', family='Cinzel')
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display warning if DSCR drops below 1.0
        if min(stress_dscr) < 1.0:
            st.error(f"🚨 CRITICAL ALERT: Portfolio breaches default threshold in Year {np.argmin(stress_dscr)+1}. Expected Loss increases by $420M.")
        else:
            st.success("✅ Portfolio demonstrates resilience to the selected macroeconomic shock.")

# -----------------------------------------
# Placeholders for other pages
# -----------------------------------------
else:
    st.title(f"⚜️ {page} ⚜️")
    st.info("Module under construction by InfraRisk AI Architecture Team.")