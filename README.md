# ✈️ Aircraft Engine Predictive Maintenance Data Pipeline

## 📌 Overview
This project implements a cloud-based data engineering pipeline for aircraft engine predictive maintenance. The system ingests real-time sensor data, processes it, and prepares it for machine learning models to predict Remaining Useful Life (RUL).

---

## 🏗️ Architecture

Pipeline Flow:

API → Lambda (Ingestion) → S3 (Raw) → Lambda (ETL) → S3 (Processed) → ML Model

Orchestrated using AWS Step Functions.

---

## ⚙️ Tech Stack

- Python
- AWS S3 (Data Lake)
- AWS Lambda (Serverless Compute)
- AWS Step Functions (Orchestration)
- Pandas (Data Processing)
- Flask (API Simulation)

---

## 🚀 Features

- Real-time data ingestion via API
- Cloud-based data lake storage
- ETL pipeline with data cleaning & transformation
- RUL (Remaining Useful Life) calculation
- Fully orchestrated workflow using Step Functions

---

## 🔄 Pipeline Components

### 1. Data Source
- Simulated API using Flask
- Provides aircraft engine sensor data

### 2. Ingestion Layer
- AWS Lambda function
- Fetches API data and stores in S3 (raw)

### 3. Data Lake
- Amazon S3 bucket
- Stores raw JSON data

### 4. ETL Layer
- AWS Lambda transformation
- Handles:
  - Missing values
  - Duplicate removal
  - Data type conversion
  - RUL calculation

### 5. Processed Storage
- Cleaned dataset stored in S3 as CSV
- Ready for machine learning

### 6. Orchestration
- AWS Step Functions
- Automates ingestion → ETL workflow

---

## 📊 Use Case

Aircraft engine maintenance prediction using sensor data to estimate Remaining Useful Life (RUL), enabling proactive maintenance and reducing failure risk.

---

## 🤖 Machine Learning Model

An XGBoost regression model is used to predict the remaining useful life (RUL) of aircraft engines.

The model is trained on historical sensor data and integrated into the pipeline for generating predictions from processed data.

---

## 🧠 Key Learnings

- Building end-to-end data pipelines
- Working with AWS cloud services
- Implementing ETL processes
- Orchestrating workflows using Step Functions

---
## 🎯 Future Improvements

- Integrate real-time streaming (Kafka / Kinesis)
- Deploy ML model for live predictions
- Replace simulated API with real-world data source

---

## 👤 Author
Dewmi Tharunya
