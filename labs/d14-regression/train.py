import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

df = pd.read_csv('data/train.csv')

X = df.select_dtypes("number").drop(columns=["Id","SalePrice"])
y = df["SalePrice"]

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

model = Pipeline([
    ("imputer", SimpleImputer(strategy="median")),
    ("model", LinearRegression()),
])

model.fit(X_train, y_train)

train_rmse = root_mean_squared_error(y_train, model.predict(X_train))
val_rmse = root_mean_squared_error(y_val, model.predict(X_val))

print(f"Train RMSE:      ${train_rmse:,.0f}")
print(f"Validation RMSE: ${val_rmse:,.0f}")
print(f"Gap:             ${val_rmse - train_rmse:,.0f}")