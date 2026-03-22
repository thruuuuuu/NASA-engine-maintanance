import requests
import boto3
import json
from datetime import datetime
import time

# -----------------------------
# CONFIG
# -----------------------------
API_URL = "http://127.0.0.1:5000/get-sensor-data"
BUCKET_NAME = "aircraft-pipeline-raw"
S3_PREFIX = "engine/raw/"

# -----------------------------
# AWS S3 CLIENT
# -----------------------------
s3 = boto3.client("s3")

# -----------------------------
# FUNCTION: FETCH FROM API
# -----------------------------
def fetch_data():
    response = requests.get(API_URL)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error fetching data")
        return None

# -----------------------------
# FUNCTION: UPLOAD TO S3
# -----------------------------
def upload_to_s3(data):
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S")

    file_name = f"{S3_PREFIX}sensor_data_{timestamp}.json"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_name,
        Body=json.dumps(data)
    )

    print(f"Uploaded: {file_name}")

# -----------------------------
# MAIN LOOP (SIMULATE STREAM)
# -----------------------------
def run_pipeline(num_records=10):
    for i in range(num_records):
        data = fetch_data()

        if data:
            upload_to_s3(data)

        time.sleep(1)  # simulate streaming delay


if __name__ == "__main__":
    run_pipeline(10)