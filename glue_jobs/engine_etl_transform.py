import boto3
import pandas as pd
import json
from io import BytesIO

# -----------------------------
# CONFIG
# -----------------------------
BUCKET_NAME = "aircraft-pipeline-raw"
RAW_PREFIX = "engine/raw/"
PROCESSED_BUCKET = "aircraft-pipeline-processed"
PROCESSED_KEY = "engine/processed/processed_data.csv"

# -----------------------------
# S3 CLIENT
# -----------------------------
s3 = boto3.client("s3")

# -----------------------------
# LOAD RAW DATA FROM S3
# -----------------------------
response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=RAW_PREFIX)

all_data = []

for obj in response.get("Contents", []):
    file_key = obj["Key"]

    file_obj = s3.get_object(Bucket=BUCKET_NAME, Key=file_key)
    file_content = file_obj["Body"].read().decode("utf-8")

    data = json.loads(file_content)
    all_data.append(data)

# Convert to DataFrame
df = pd.DataFrame(all_data)

print("Raw Data Shape:", df.shape)

# -----------------------------
# DATA CLEANING
# -----------------------------

# 1. Remove duplicates
df = df.drop_duplicates()

# 2. Handle missing values
df = df.fillna(df.mean(numeric_only=True))

# 3. Data type conversion
for col in df.columns:
    if col not in ["engine_id", "cycle"]:
        df[col] = df[col].astype(float)

# -----------------------------
# DATA TRANSFORMATION
# -----------------------------

# Compute max cycle per engine
max_cycle = df.groupby("engine_id")["cycle"].max()

df = df.merge(max_cycle, on="engine_id", suffixes=("", "_max"))

# Compute RUL
df["RUL"] = df["cycle_max"] - df["cycle"]

# Optional: cap RUL
df["RUL"] = df["RUL"].clip(upper=130)

# -----------------------------
# SAVE TO S3 (PROCESSED)
# -----------------------------

csv_buffer = BytesIO()
df.to_csv(csv_buffer, index=False)

s3.put_object(
    Bucket=PROCESSED_BUCKET,
    Key=PROCESSED_KEY,
    Body=csv_buffer.getvalue()
)

print("Processed data uploaded successfully!")