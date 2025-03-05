import pandas as pd
import streamlit as st
import plotly.express as px
import dask.dataframe as dd

# Streamlit App Title
st.title("🚖 Uber Data Analytics Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload your Uber dataset (CSV format)", type=["csv"])

if uploaded_file is not None:
    @st.cache_data
    def load_data(file):
        df = dd.read_csv(file)  # Use Dask for large datasets
        df["START_DATE"] = dd.to_datetime(df["START_DATE"], format="%m/%d/%Y %H:%M", errors='coerce')
        df["END_DATE"] = dd.to_datetime(df["END_DATE"], format="%m/%d/%Y %H:%M", errors='coerce')
        df["TRIP_DURATION"] = (df["END_DATE"] - df["START_DATE"]).dt.total_seconds() / 60
        df["PURPOSE"] = df["PURPOSE"].fillna("Unknown")
        return df.compute()  # Convert Dask DataFrame to Pandas

    df = load_data(uploaded_file)
    
    # Show sample data
    if st.checkbox("Show Sample Data"):
        st.write(df.sample(100))  # Display only 100 random rows for preview

    # Sidebar filters
    st.sidebar.header("Filter Data")
    start_date = st.sidebar.date_input("Start Date", df["START_DATE"].min().date())
    end_date = st.sidebar.date_input("End Date", df["END_DATE"].max().date())

    @st.cache_data
    def filter_data(start_date, end_date):
        return df.query("START_DATE >= @start_date and END_DATE <= @end_date")

    df_filtered = filter_data(start_date, end_date)

    # Visualizations
    fig1 = px.line(df_filtered, x="START_DATE", y="MILES", title="Miles Traveled Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(df_filtered, x="TRIP_DURATION", title="Trip Duration Distribution", nbins=50)
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Please upload a CSV file to proceed.")
