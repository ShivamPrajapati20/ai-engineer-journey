"""Day 07 - EDA on the Telco Customer Churn dataset.

Data: https://www.kaggle.com/datasets/blastchar/telco-customer-churn
Save the CSV as labs/d07-pandas/data/telco.csv (not committed - see .gitignore).
Run from the repo root:  python labs/d07-pandas/explore.py
"""

import pandas as pd

df = pd.read_csv("labs/d07-pandas/data/telco.csv")

# --- Task 1: first look ---
print("shape:", df.shape)
print(df.dtypes)
print(df.describe())
print("nulls per column:\n", df.isna().sum())

# --- Task 2: clean TotalCharges (11 blanks = tenure-0 customers, not billed yet -> 0) ---
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)
print("TotalCharges:", df["TotalCharges"].dtype, "NaN:", df["TotalCharges"].isna().sum())

# --- Task 3: churn rate by segment ---
df["churned"] = (df["Churn"] == "Yes").astype(int)
df["tenure_bucket"] = pd.cut(df["tenure"], bins=[-1, 12, 24, 48, 72],
                             labels=["0-12", "13-24", "25-48", "49+"])

print("overall churn:", round(df["churned"].mean(), 3))
for col in ["Contract", "InternetService", "tenure_bucket"]:
    table = (df.groupby(col, observed=True)["churned"]
               .agg(["mean", "count"])
               .sort_values("mean", ascending=False))
    print(f"\nchurn by {col}:\n{table}")
