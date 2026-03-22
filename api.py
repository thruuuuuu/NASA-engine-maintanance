from flask import Flask, jsonify
import pandas as pd
import random

app = Flask(__name__)

# Load dataset
columns = ["engine_id", "cycle",
           "op1", "op2", "op3"] + \
          [f"sensor{i}" for i in range(1, 22)]

df = pd.read_csv(r"data\train_FD001.txt", sep=r"\s+", header=None)
df.columns = columns

@app.route("/get-sensor-data", methods=["GET"])
def get_data():
    # pick random row (simulate live data)
    row = df.sample(1).to_dict(orient="records")[0]
    return jsonify(row)

if __name__ == "__main__":
    app.run(debug=True)