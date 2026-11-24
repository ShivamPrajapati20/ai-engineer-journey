import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

df = pd.read_csv("data/train.csv")
y = df["SalePrice"]

# Numbers + our winning feature from Task 3
num_cols = df.select_dtypes("number").drop(columns=["Id", "SalePrice"]).columns.tolist()
X = df[num_cols + ["Neighborhood"]].assign(QualxSF=df["OverallQual"] * df["GrLivArea"])
num_cols = num_cols + ["QualxSF"]

# Traffic police: numbers -> imputer, Neighborhood -> one-hot
prep = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["Neighborhood"]),
])

model = Pipeline([
    ("prep", prep),
    ("model", LinearRegression()),
])

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
model.fit(X_train, y_train)

train_rmse = root_mean_squared_error(y_train, model.predict(X_train))
val_rmse = root_mean_squared_error(y_val, model.predict(X_val))
print(f"Train RMSE:      ${train_rmse:,.0f}")
print(f"Validation RMSE: ${val_rmse:,.0f}   (Task 3 was $34,331)")

# Production test: a brand-new neighborhood the model never saw
row = X_val.iloc[[0]].copy()
row["Neighborhood"] = "Mars"
print(f"New neighborhood 'Mars' -> ${model.predict(row)[0]:,.0f}  (no crash)")