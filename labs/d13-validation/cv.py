"""Day 13 - 5-fold cross-validation on the Day 12 model."""

from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

data = load_breast_cancer()
X = data.data
y = (data.target == 0).astype(int)            # 1 = malignant (cancer)

# Lock the test set away. Cross-validation only uses the training part.
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))

for metric in ["accuracy", "recall"]:
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring=metric)
    print(f"{metric:8}: {scores.round(3)}  ->  {scores.mean():.3f} +/- {scores.std():.3f}")