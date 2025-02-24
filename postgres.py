import pandas as pd
import streamlit as st
import plotly.express as px
import dask.dataframe as dd
from sqlalchemy import create_engine
import psycopg2

# PostgreSQL Database Connection
DB_USER = "postgres"
DB_PASSWORD = "admin123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mydash"
TABLE_NAME = "uber_rides"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Function to load data from uploaded file and store in PostgreSQL
@st.cache_data
def load_and_store_data(uploaded_file):
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        
        # Convert date columns
        df["START_DATE"] = pd.to_datetime(df["START_DATE"], errors='coerce')
        df["END_DATE"] = pd.to_datetime(df["END_DATE"], errors='coerce')
        df["TRIP_DURATION"] = (df["END_DATE"] - df["START_DATE"]).dt.total_seconds() / 60
        df["PURPOSE"] = df["PURPOSE"].fillna("Unknown")
        
        # Store into PostgreSQL
        df.to_sql(TABLE_NAME, engine, if_exists='replace', index=False)
        
        return df
    return None

# Streamlit UI
st.set_page_config(page_title="Uber Data Dashboard", layout="wide")
st.title("🚖 Uber Data Analytics Dashboard")

# Sidebar Filters & UI Enhancements
st.sidebar.header("📊 Filter Options")
uploaded_file = st.sidebar.file_uploader("📂 Upload CSV File", type=["csv"])
df = load_and_store_data(uploaded_file)

if df is not None:
    # Date range selection
    start_date = st.sidebar.date_input("Start Date", df["START_DATE"].min().date())
    end_date = st.sidebar.date_input("End Date", df["END_DATE"].max().date())
    
    # Category selection
    category_filter = st.sidebar.multiselect("Select Trip Purpose", df["PURPOSE"].unique())
    
    # Slider for histogram bins
    nbins = st.sidebar.slider("Histogram Bins", min_value=10, max_value=100, value=50, step=10)
    
    @st.cache_data
    def filter_data(start_date, end_date, category_filter):
        filtered_df = df.query("START_DATE >= @start_date and END_DATE <= @end_date")
        if category_filter:
            filtered_df = filtered_df[filtered_df["PURPOSE"].isin(category_filter)]
        return filtered_df
    
    df_filtered = filter_data(start_date, end_date, category_filter)
    
    # Layout using columns
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = px.line(df_filtered, x="START_DATE", y="MILES", title="Miles Traveled Over Time")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.histogram(df_filtered, x="TRIP_DURATION", title="Trip Duration Distribution", nbins=nbins)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Pie chart for trip purpose distribution
    fig3 = px.pie(df_filtered, names="PURPOSE", title="Trip Purpose Distribution")
    st.plotly_chart(fig3, use_container_width=True)
    
    # Summary Metrics
    st.subheader("📌 Key Metrics")
    col1, col2, col3 = st.columns(3)
    
    col1.metric("Total Rides", len(df_filtered))
    col2.metric("Avg Miles per Trip", round(df_filtered["MILES"].mean(), 2))
    col3.metric("Avg Trip Duration (min)", round(df_filtered["TRIP_DURATION"].mean(), 2))
    
    # Dark Mode Styling
    st.markdown(
        """
        <style>
        body {
            background-color: #0E1117;
            color: white;
        }
        .stApp {
            background-color: #0E1117;
        }
        .sidebar .sidebar-content {
            background-color: #161B22;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    
else:
    st.warning("📌 Please upload a CSV file to proceed.")
