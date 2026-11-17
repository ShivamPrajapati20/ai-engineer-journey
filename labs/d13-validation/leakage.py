"""Day 13 - naive scaling (leaky) vs Pipeline (correct) in cross-validation."""

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

data = load_breast_cancer()
X = data.data
y = (data.target == 0).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# NAIVE: scaler sees ALL training rows, including each fold's validation part
X_scaled = StandardScaler().fit_transform(X_train)
naive = cross_val_score(LogisticRegression(max_iter=1000), X_scaled, y_train, cv=5, scoring="recall")

# PIPELINE: scaler is fit inside each fold, only on that fold's training part
pipe = Pipeline([
    ("scaler", StandardScaler()),
    ("clf", LogisticRegression(max_iter=1000)),
])
correct = cross_val_score(pipe, X_train, y_train, cv=5, scoring="recall")

print(f"Naive   : {naive.mean():.4f} +/- {naive.std():.4f}")
print(f"Pipeline: {correct.mean():.4f} +/- {correct.std():.4f}")