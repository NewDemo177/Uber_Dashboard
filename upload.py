import pandas as pd
import streamlit as st
import plotly.express as px
import dask.dataframe as dd
from sqlalchemy import create_engine
import psycopg2

# PostgreSQL Connection Details
DB_URI = "postgresql://postgres:admin123@localhost:5432/mydash"

# Function to upload and load data
def load_data(file):
    df = pd.read_csv(file)
    
    # Print uploaded data to terminal
    print("\nUploaded CSV Data:\n", df.head(10))  # Print first 10 rows
    
    # Convert datetime columns
    df["START_DATE"] = pd.to_datetime(df["START_DATE"], errors="coerce")
    df["END_DATE"] = pd.to_datetime(df["END_DATE"], errors="coerce")
    
    # Fill missing values
    df["PURPOSE"] = df["PURPOSE"].fillna("Unknown")
    
    return df

# Streamlit App
st.title("🚖 Uber Data Analytics Dashboard")

# File uploader
uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])
if uploaded_file is not None:
    df = load_data(uploaded_file)  # Load and clean data

    # Display data on UI
    st.write("### Uploaded Data Preview")
    st.write(df.head(10))  # Show first 10 rows

    # Store data into PostgreSQL
    engine = create_engine(DB_URI)
    df.to_sql("uber_rides", engine, if_exists="replace", index=False)
    st.success("✅ Data stored in PostgreSQL successfully!")

    # Visualizations
    fig1 = px.line(df, x="START_DATE", y="MILES", title="Miles Traveled Over Time")
    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.histogram(df, x="TRIP_DURATION", title="Trip Duration Distribution", nbins=50)
    st.plotly_chart(fig2, use_container_width=True)
