import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

# Set page config
st.set_page_config(layout="wide")

# Load the CSV data
@st.cache_data
def load_data():
    # Read the CSV file into a DataFrame
    return pd.read_csv("data1.csv")

data = load_data()

custom_css = """
<style>
    ..st-emotion-cache-z5fcl4{
        padding-block: 20px;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar Filters
with st.sidebar:
    st.title("Law Firms Data")
    st.header("Filters")

    # Dropdown for Panel Firm
    panel_firm_options = ["All"] + list(data['Panel Firm'].unique())
    selected_panel_firm = st.selectbox("Filter by Panel Firm", panel_firm_options)
    if selected_panel_firm != "All":
        data = data[data['Panel Firm'] == selected_panel_firm]

    # Dropdown for Panel Type
    panel_type_options = ["All"] + list(data['Panel Type'].unique())
    selected_panel_type = st.selectbox("Filter by Panel Type", panel_type_options)
    if selected_panel_type != "All":
        data = data[data['Panel Type'] == selected_panel_type]

    # Multi-select for Practice Areas/Group
    all_practice_areas = list(set(", ".join(data['Practice Areas/Group'].dropna()).split(", ")))
    selected_practice_areas = st.multiselect("Filter by Practice Areas/Group", all_practice_areas)

    if not selected_practice_areas:
        selected_practice_areas = all_practice_areas

    data = data[data['Practice Areas/Group'].apply(lambda x: any(area in x for area in selected_practice_areas) if pd.notnull(x) else False)]

   

# Display data using AgGrid
AgGrid(data)
