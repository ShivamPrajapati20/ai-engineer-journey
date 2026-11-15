"""Day 12 - ROC curve, AUC, and choosing a threshold for recall >= 0.95."""

import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_breast_cancer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (classification_report, confusion_matrix, precision_score,
                             recall_score, roc_auc_score, roc_curve)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

# 1. Data. In sklearn, 0 = malignant, 1 = benign.
#    We want "positive" = cancer, so flip it: 1 = malignant.
data = load_breast_cancer()
X = data.data
y = (data.target == 0).astype(int)

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 2. Train (scale first, so logistic regression trains well)
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000))
model.fit(X_train, y_train)

# 3. Probabilities, not yes/no
probs = model.predict_proba(X_test)[:, 1]          # chance of cancer for each patient

# 4. Default threshold 0.5
default = (probs >= 0.5).astype(int)
print("Threshold 0.50 -> precision", round(precision_score(y_test, default), 3),
      "recall", round(recall_score(y_test, default), 3))

# 5. ROC curve + AUC
fpr, tpr, thresholds = roc_curve(y_test, probs)
auc = roc_auc_score(y_test, probs)
print("AUC:", round(auc, 3))

# 6. First (highest) threshold that reaches recall >= 0.95
idx = np.where(tpr >= 0.95)[0][0]
chosen = thresholds[idx]
picked = (probs >= chosen).astype(int)
print(f"Threshold {chosen:.3f} -> precision", round(precision_score(y_test, picked), 3),
      "recall", round(recall_score(y_test, picked), 3))
print("Confusion matrix [TN FP FN TP]:", confusion_matrix(y_test, picked).ravel())

# 7. Plot
plt.plot(fpr, tpr, label=f"Logistic regression (AUC = {auc:.3f})")
plt.plot([0, 1], [0, 1], "--", label="Coin flip")
plt.scatter(fpr[idx], tpr[idx], color="red", zorder=3, label=f"Chosen threshold {chosen:.2f}")
plt.xlabel("False positive rate (healthy flagged)")
plt.ylabel("True positive rate (recall)")
plt.title("ROC curve - breast cancer")
plt.legend()
plt.savefig("labs/d12-classification/roc.png", dpi=120)
print("Saved roc.png")