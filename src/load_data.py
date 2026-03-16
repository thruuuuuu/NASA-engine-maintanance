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