# 🏢 Hostel Utility Management & Analytics

A robust management application designed to track and automate utility expenses (electricity, water, Wi-Fi) for hostel residents based on usage logs.

## ✨ Key Features
- **Dual-Mode Input:** Supports manual entry for single records and bulk CSV uploads for large-scale processing.
- **Automated Billing:** Reduces manual accounting errors by applying dynamic tariff rates to consumption data.
- **Proactive Validation:** Robust exception handling flags non-numeric entries (like text) and negative usage values before calculation.
- **Interactive Analytics:** Visualizes room-wise bill distribution and total revenue metrics using Plotly dashboards.
- **Structured Export:** Generates detailed JSON reports summarizing individual student dues for administrative use.

## 🛠️ Implementation Details
- **Frontend:** Streamlit
- **Data Engine:** Pandas
- **Visuals:** Plotly
- **Validation:** Utilizes `pd.to_numeric` with error coercion to prevent system crashes during bulk uploads.

## 🚀 How to Run
1. Install requirements: `pip install streamlit pandas plotly`
2. Run the application: `streamlit run app.py`
