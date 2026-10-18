import pandas as pd

df = pd.read_csv("data/telco.csv")

#1: first look
print("shape:", df.shape)
print("Type:", df.dtypes)
print("Describe:", df.describe())
print("nulls per column:\n", df.isna().sum())

#2: clean
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"],errors="coerce").fillna(0)
print("TotalCharges:", df["TotalCharges"].dtype, df["TotalCharges"].isna().sum())

#3: churn rate
df["churned"] = (df["Churn"] == "Yes").astype(int)
df["tenure_bucket"] = pd.cut(df["tenure"], bins=[-1,12,24,48,72],
                            labels=["0-12","13-24","25-48","49+"])

print("Overall churn:", round(df["churned"].mean(),3))

for col in ["Contract","InternetService","tenure_bucket"]:
    table = (df.groupby(col, observed=True)["churned"]
             .agg(["mean","count"])
             .sort_values("mean", ascending=False))
    print(f"\nChurn by {col}:\n{table}")