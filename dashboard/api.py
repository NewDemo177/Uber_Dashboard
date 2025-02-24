from flask import Flask, request, jsonify
import pandas as pd
from sqlalchemy import create_engine

app = Flask(__name__)

# PostgreSQL connection
DB_USER = "postgres"
DB_PASSWORD = "admin123"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "mydash"
TABLE_NAME = "uber_rides"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# 📌 API to GET all Uber rides data
@app.route("/get-data", methods=["GET"])
def get_data():
    query = f"SELECT * FROM {TABLE_NAME} LIMIT 100;"  # Fetch sample data
    df = pd.read_sql(query, engine)
    return jsonify(df.to_dict(orient="records"))

# 📌 API to UPLOAD CSV and store in PostgreSQL
@app.route("/upload-data", methods=["POST"])
def upload_data():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    df = pd.read_csv(file)
    
    # Convert date columns
    df["START_DATE"] = pd.to_datetime(df["START_DATE"], errors='coerce')
    df["END_DATE"] = pd.to_datetime(df["END_DATE"], errors='coerce')
    df["TRIP_DURATION"] = (df["END_DATE"] - df["START_DATE"]).dt.total_seconds() / 60
    df["PURPOSE"] = df["PURPOSE"].fillna("Unknown")
    
    # Store in database
    df.to_sql(TABLE_NAME, engine, if_exists='append', index=False)
    
    return jsonify({"message": "File uploaded successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True)
