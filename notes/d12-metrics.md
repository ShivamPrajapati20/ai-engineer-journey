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
