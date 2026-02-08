import streamlit as st
import pandas as pd
import plotly.express as px
import json

# --- 1. UI STYLING (Large Fonts) ---
st.set_page_config(page_title="Hostel Utility Pro", layout="wide")

st.markdown("""
    <style>
    html, body, [class*="css"] { font-size: 22px !important; }
    .stMetric { font-size: 32px !important; }
    h1 { font-size: 55px !important; }
    h2 { font-size: 45px !important; }
    h3 { font-size: 35px !important; }
    button p { font-size: 24px !important; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏢 Hostel Utility Management & Analytics")

# --- 2. TARIFF CONFIGURATION (Sidebar) ---
with st.sidebar:
    st.header("Tariff Settings")
    e_rate = st.number_input("Electricity Rate (per unit)", value=8.53)
    w_rate = st.number_input("Water Rate (per unit)", value=12.0)
    wifi_fixed = st.number_input("Fixed Wi-Fi Fee", value=500.0)

# --- 3. PROCESSING FUNCTION ---
def display_results(df, report_type):
    """Calculates and shows results ONLY for the active data."""
    # Exception Handling: Check for negative values
    if (df[['electricity_usage', 'water_usage']] < 0).any().any():
        st.error("🚨 Error: Negative usage values detected! Please correct them.")
        return

    # Calculations
    df['Electricity Cost'] = df['electricity_usage'] * e_rate
    df['Water Cost'] = df['water_usage'] * w_rate
    df['Total Bill'] = df['Electricity Cost'] + df['Water Cost'] + wifi_fixed

    # Visuals
    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Bill Distribution")
        fig = px.bar(df, x="room_id", y="Total Bill", color="Total Bill", template="plotly_dark")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        st.subheader("Summary Metrics")
        st.metric("Total Revenue", f"₹{df['Total Bill'].sum():,.2f}")
        st.metric("Avg Bill", f"₹{df['Total Bill'].mean():,.2f}")

    st.dataframe(df.style.highlight_max(axis=0, subset=['Total Bill']))
    
    # JSON Export
    json_str = df.to_json(orient="records", indent=4)
    st.download_button(f"📥 Export {report_type} JSON", json_str, f"{report_type}.json")

# --- 4. INDEPENDENT TABS ---
tab1, tab2 = st.tabs(["📤 Bulk CSV Upload", "📝 Manual Entry"])

with tab1:
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        csv_df = pd.read_csv(uploaded_file)
        display_results(csv_df, "Bulk_Report")
    else:
        st.info("Upload a file to see Bulk results.")

with tab2:
    # We move the results OUTSIDE the form to avoid the error
    with st.form("entry_form"):
        r_id = st.text_input("Room ID")
        e_u = st.number_input("Elec Usage", min_value=0.0)
        w_u = st.number_input("Water Usage", min_value=0.0)
        submitted = st.form_submit_button("Calculate Bill")
    
    if submitted:
        manual_df = pd.DataFrame([{"room_id": r_id, "electricity_usage": e_u, "water_usage": w_u}])
        display_results(manual_df, "Manual_Report")