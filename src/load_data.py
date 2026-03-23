import pandas as pd
import numpy as np

# -------------------------------
# 1. LOAD DATA
# -------------------------------
columns = ["engine_id", "cycle",
           "op1", "op2", "op3"] + \
          [f"sensor{i}" for i in range(1, 22)]

df = pd.read_csv("../data/train_FD001.txt", sep="\s+", header=None)
df.columns = columns

# -------------------------------
# 2. CREATE RUL
# -------------------------------
max_cycle = df.groupby("engine_id")["cycle"].max()
df = df.merge(max_cycle, on="engine_id", suffixes=("", "_max"))

df["RUL"] = df["cycle_max"] - df["cycle"]

# 🔥 IMPORTANT: cap RUL (improves model a lot)
df["RUL"] = df["RUL"].clip(upper=130)

# -------------------------------
# 3. REMOVE USELESS COLUMNS
# -------------------------------
# remove constant columns
df = df.loc[:, df.nunique() > 1]

# -------------------------------
# 4. ENGINE-LEVEL SPLIT (CRITICAL)
# -------------------------------
from sklearn.model_selection import train_test_split

engine_ids = df["engine_id"].unique()

train_engines, test_engines = train_test_split(
    engine_ids, test_size=0.2, random_state=42
)

train_df = df[df["engine_id"].isin(train_engines)]
test_df = df[df["engine_id"].isin(test_engines)]

# -------------------------------
# 5. FEATURES & TARGET
# -------------------------------
X_train = train_df.drop(["RUL", "engine_id", "cycle", "cycle_max"], axis=1)
y_train = train_df["RUL"]

X_test = test_df.drop(["RUL", "engine_id", "cycle", "cycle_max"], axis=1)
y_test = test_df["RUL"]

# -------------------------------
# 6. SCALE DATA (PROPER WAY)
# -------------------------------
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# -------------------------------
# 7. TRAIN MODEL (XGBOOST)
# -------------------------------
from xgboost import XGBRegressor

model = XGBRegressor(
    n_estimators=500,
    learning_rate=0.03,
    max_depth=6,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42
)

model.fit(X_train, y_train)

# -------------------------------
# 8. PREDICT & EVALUATE
# -------------------------------
from sklearn.metrics import mean_absolute_error

predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)

print("\nFinal MAE:", mae)

# -------------------------------
# 9. FEATURE IMPORTANCE
# -------------------------------
importance = model.feature_importances_

feature_names = train_df.drop(
    ["RUL", "engine_id", "cycle", "cycle_max"], axis=1
).columns

importance_df = pd.DataFrame({
    "Feature": feature_names,
    "Importance": importance
}).sort_values(by="Importance", ascending=False)

print("\nTop Features:\n")
print(importance_df.head(10))