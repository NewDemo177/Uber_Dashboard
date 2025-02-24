import streamlit as st
import requests
import pandas as pd

st.title("📊 Uber Data API Interface")

# Fetch data button
if st.button("Fetch Uber Data"):
    response = requests.get("http://127.0.0.1:5000/get-data")
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        st.write(df)
    else:
        st.error("Failed to fetch data.")

# File uploader for CSV upload
uploaded_file = st.file_uploader("Upload a CSV file to API", type=["csv"])
if uploaded_file is not None:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post("http://127.0.0.1:5000/upload-data", files=files)
    if response.status_code == 200:
        st.success("File uploaded successfully!")
    else:
        st.error("Upload failed.")
