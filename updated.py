import streamlit as st
import pandas as pd
import plotly.express as px

# Load the data
df = pd.read_csv("/home/kundan/Downloads/cleaned_data.csv")

# Streamlit Page Configurations
st.set_page_config(page_title="Uber Data Analytics Dashboard", layout="wide")

# Sidebar for Filters
st.sidebar.header("Filters")
category_filter = st.sidebar.selectbox("Select Trip Category:", df["CATEGORY"].unique())
date_range = st.sidebar.date_input("Select Date Range:", [])

# Apply Filters
df_filtered = df[df["CATEGORY"] == category_filter]

# Dashboard Layout using Columns
st.title("🚖 Uber Data Analytics Dashboard")

with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Trip Duration Distribution")
        fig1 = px.histogram(df_filtered, x="MILES", title="Miles Distribution", nbins=50)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.subheader("Trip Purpose Breakdown")
        fig2 = px.pie(df_filtered, names="PURPOSE", title="Trip Purpose Distribution")
        st.plotly_chart(fig2, use_container_width=True)

# Custom Styling
st.markdown("""
    <style>
        .main {
            background-color: #f4f4f4;
        }
        .stTitle {
            color: #1f77b4;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

