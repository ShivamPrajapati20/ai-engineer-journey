import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import root_mean_squared_error

df = pd.read_csv("data/train.csv")
y = df["SalePrice"]
X = df.select_dtypes("number").drop(columns=["Id", "SalePrice"])


def val_rmse(X):
    """Train on 80%, return the error on the other 20%."""
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    model = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("model", LinearRegression()),
    ])
    model.fit(X_train, y_train)
    return root_mean_squared_error(y_val, model.predict(X_val))


print(f"Baseline:  ${val_rmse(X):,.0f}")

# Clue 1: age of the house  (a - b)
X1 = X.assign(HouseAge=df["YrSold"] - df["YearBuilt"])
print(f"+HouseAge: ${val_rmse(X1):,.0f}")

# Clue 2: total area  (a + b + c)
X2 = X.assign(TotalSF=df["TotalBsmtSF"] + df["1stFlrSF"] + df["2ndFlrSF"])
print(f"+TotalSF:  ${val_rmse(X2):,.0f}")

# Clue 3: quality x size  (a × b)
X3 = X.assign(QualxSF=df["OverallQual"] * df["GrLivArea"])
print(f"+QualxSF:  ${val_rmse(X3):,.0f}")