import streamlit as st
import pandas as pd
from st_aggrid import AgGrid

# Set page config
st.set_page_config(layout="wide")

# Load the CSV data
@st.cache_data
def load_data():
    return pd.read_csv("data1.csv")

data = load_data()
orig_data = data.copy()

custom_css = """
<style>
.st-emotion-cache-z5fcl4{
padding-block: 20px;
}
    body {
        color: #11a4cd;
        background-color: #ffdf04;
    }
    .stSidebar {
        background-color: #11a4cd;
        color: #ffdf04;
    }
    .stButton>button {
        background-color: #ffdf04;
        color: #11a4cd;
        border: 2px solid #11a4cd;
        
    }
     .stButton>button:hover {
        background-color: yellow;
        color: #11a4cd;
        border: 2px solid #11a4cd;
        
    }
    select, option {
        color: #11a4cd;
        background-color: #ffdf04;
    }
</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)

default_panel_firm = "All"
default_panel_type = "All"
default_practice_areas = list(set(", ".join(data['Practice Areas/Group'].dropna()).split(", ")))

# Sidebar Filters
with st.sidebar:
    st.title("Global Authorized Outside Counsel List")
    st.header("Filters")

    panel_firm_options = ["All"] + list(data['Panel Firm'].unique())
    selected_panel_firm = st.selectbox("Filter by Panel Firm", panel_firm_options)
    if selected_panel_firm != "All":
        data = data[data['Panel Firm'] == selected_panel_firm]

    panel_type_options = ["All"] + list(data['Panel Type'].unique())
    selected_panel_type = st.selectbox("Filter by Panel Type", panel_type_options)
    if selected_panel_type != "All":
        data = data[data['Panel Type'] == selected_panel_type]

    all_practice_areas = list(set(", ".join(data['Practice Areas/Group'].dropna()).split(", ")))
    selected_practice_areas = st.multiselect("Filter by Practice Areas/Group", all_practice_areas)
    if not selected_practice_areas:
        selected_practice_areas = all_practice_areas

    data = data[data['Practice Areas/Group'].apply(lambda x: any(area in x for area in selected_practice_areas) if pd.notnull(x) else False)]

    reload_data = False
    if st.button('Reset Inputs'):
        
        data = orig_data.copy()
        selected_panel_firm = "All"
        selected_panel_type = "All"
        selected_practice_areas = all_practice_areas
       
        reload_data = True
        
# Display data using AgGrid
AgGrid(data, reload_data=reload_data)
