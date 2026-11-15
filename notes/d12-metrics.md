# Day 12: Classification and the metrics that matter

## Task 1: Thresholds and the confusion matrix

- A classifier outputs a **probability**. The **threshold** turns it into yes/no.
- Lower threshold → flag more → catch more, but more false alarms. Higher threshold → the opposite.
- 0.5 is only a default. The business picks the threshold based on what each mistake costs.

|  | Model says YES | Model says NO |
|---|---|---|
| **Really YES** | TP (correct catch) | FN (missed it) |
| **Really NO** | FP (false alarm) | TN (correct pass) |

### Fraud model (YES = block the card)

|  | Model: FRAUD (block) | Model: OK (allow) |
|---|---|---|
| **Really fraud** | **TP:** stolen money saved (~$500). Customer trusts the bank more. | **FN:** bank refunds the stolen money (~$500 to $2,000), fraud team time, customer loses trust. |
| **Really OK** | **FP:** real customer declined at checkout, support call (~$10), some switch banks. | **TN:** $0, normal happy customer. |

**Worse mistake:** FN (big money loss per case) → lower the threshold to catch more fraud, but not so low that real customers get blocked all the time. Banks soften FP by texting "Was this you?" instead of only blocking.

## Task 2: Accuracy, precision, recall

| Metric | Question | Formula |
|---|---|---|
| **Accuracy** | Out of all predictions, how many were right? | (TP + TN) / all |
| **Precision** | When the model says yes, how often is it right? ("don't cry wolf") | TP / (TP + FP) |
| **Recall** | Out of all real yes cases, how many did it catch? ("don't miss any") | TP / (TP + FN) |
| **F1** | Balance of precision and recall | 2·P·R / (P + R) |

### The accuracy trap (my words)

If the class is rare, don't trust accuracy. On a 99.8%-negative dataset, a model that always says "no" gets 99.8% accuracy but catches nothing (recall = 0). Use **recall** when misses are costly, **precision** when false alarms are costly.

### Support-ticket router (my words)

If something is important and urgent, optimize **recall** (on the urgent/outage class), because missing a real outage loses customers, while a false urgent flag only costs an engineer a few minutes.

| Question | Answer |
|---|---|
| Worse mistake? | Missing an urgent ticket |
| Which error is that? | FN |
| Metric that reduces FN? | Recall |

## Task 3: ROC, AUC, and threshold selection

Code: [`labs/d12-classification/roc.py`](../labs/d12-classification/roc.py) · Plot: [`roc.png`](../labs/d12-classification/roc.png)

- **ROC curve** = recall (true positive rate) vs false alarm rate, one point per threshold. Top-left corner = perfect, diagonal = coin flip.
- **AUC** = area under the ROC curve, one score across all thresholds (1.0 perfect, 0.5 useless). It is the chance the model scores a random positive higher than a random negative.
- Business rule for cancer screening: catch at least 95% of cancers (recall ≥ 0.95), because a missed cancer (FN) is far worse than an extra test (FP).

### Results (breast cancer dataset, positive = malignant, 114 test patients: 42 cancer, 72 healthy)

| Threshold | Precision | Recall | Cancers missed (FN) |
|---|---|---|---|
| 0.50 (default) | 0.975 | 0.929 (below 0.95) | 3 |
| **0.315 (chosen)** | **0.976** | **0.976** | **1** |

- AUC = **0.996**.
- Confusion matrix at 0.315: TN 71, FP 1, FN 1, TP 41 → only 2 mistakes out of 114.
- **Answer:** threshold 0.315 → precision 0.976, recall 0.976. Lowering the threshold from 0.5 caught 2 more cancers.
- Precision did not drop here because this dataset is very easy (AUC 0.996). On real, messy data, raising recall usually costs precision, and the business decides how much it can accept.

## Task 4: Reading a classification report

```python
print(classification_report(y_test, predictions, target_names=["benign", "malignant"]))
```

### Report at the default threshold 0.5

```
              precision    recall  f1-score   support

      benign       0.96      0.99      0.97        72
   malignant       0.97      0.93      0.95        42

    accuracy                           0.96       114
   macro avg       0.97      0.96      0.96       114
weighted avg       0.97      0.96      0.96       114
```

At the chosen threshold 0.315 every number goes up to 0.98 to 0.99 (only 2 mistakes).

### Each column (malignant row, in my words)

| Column | Meaning |
|---|---|
| **precision 0.97** | Of the patients the model called cancer, 97% really had cancer. |
| **recall 0.93** | Of the 42 real cancer patients, the model caught 93% (39 caught, 3 missed). |
| **f1-score 0.95** | One number that balances precision and recall. |
| **support 42** | There were 42 real cancer patients in the test set. |

Precision and recall measure different things, so they are not compared with each other.

### Bottom 3 lines

| Line | Meaning |
|---|---|
| **accuracy** | Correct predictions out of all 114. |
| **macro avg** | Simple average of the classes: every class counts the same. |
| **weighted avg** | Average weighted by support: bigger classes count more. |

### Macro vs weighted (my words)

On imbalanced data we use **macro**, because a small class can hide inside the weighted average. If we want the overall result group-wise (weighted by how many cases each class has), **weighted** is better.

Example (990 OK, 10 fraud, model catches 2 frauds): weighted F1 = 0.99 (looks great), macro F1 = 0.66 (shows fraud detection is failing).

| Use | When |
|---|---|
| **Macro** | Every class matters equally, especially a small important class (fraud, cancer, urgent tickets) |
| **Weighted** | You want the overall result, and bigger classes matter more |
| **Micro** | Every single prediction counts the same; in normal multi-class problems it equals accuracy |

If macro is much lower than weighted, some small class is failing: check its row.
