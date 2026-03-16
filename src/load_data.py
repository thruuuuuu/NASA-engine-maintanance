import pandas as pd

# Column names for dataset
columns = ["engine_id", "cycle",
           "op1", "op2", "op3"] + \
          [f"sensor{i}" for i in range(1, 22)]

# Load dataset
df = pd.read_csv(
    "../data/train_FD001.txt",
    sep="\s+",
    header=None
)

df.columns = columns

# Show first rows
print(df.head())

# Basic info
print("\nDataset Info:\n")
print(df.info())

# Shape
print("\nDataset Shape:", df.shape)

# Number of unique engines
print("Total Engines:", df["engine_id"].nunique())

# Max cycle per engine
engine_life = df.groupby("engine_id")["cycle"].max()

print("\nEngine Life Statistics")
print(engine_life.describe())

# Compute max cycle per engine
max_cycle = df.groupby("engine_id")["cycle"].max()

# Merge back to dataframe
df = df.merge(max_cycle, on="engine_id", suffixes=("", "_max"))

# Calculate Remaining Useful Life
df["RUL"] = df["cycle_max"] - df["cycle"]

# Preview
print(df[["engine_id","cycle","cycle_max","RUL"]].head(10))

import matplotlib.pyplot as plt

'''select one engine
engine1 = df[df["engine_id"] == 1]

# plot sensor trend
plt.plot(engine1["cycle"], engine1["sensor12"])

plt.xlabel("Cycle")
plt.ylabel("Sensor 12 Value")
plt.title("Engine 1 Degradation Trend")

plt.show()'''

# correlation with RUL
correlation = df.corr()["RUL"].sort_values()

print("\nSensor Correlation with RUL:\n")
print(correlation)

# remove columns with no variation
df = df.loc[:, df.nunique() > 1]
'''
import seaborn as sns
import matplotlib.pyplot as plt

plt.figure(figsize=(12,8))

sns.heatmap(df.corr(), cmap="coolwarm")

plt.title("Sensor Correlation Heatmap")

plt.show()'''

# target variable
y = df["RUL"]

# remove non-feature columns
X = df.drop(["RUL", "engine_id", "cycle", "cycle_max"], axis=1)

print("Feature shape:", X.shape)
print("Target shape:", y.shape)