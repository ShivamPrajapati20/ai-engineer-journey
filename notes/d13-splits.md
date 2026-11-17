# Day 13: Training, validation, testing and overfitting

## Task 1: Why a validation set exists

### Overfitting

- **Overfitting** = the model memorizes the training data (like a student who memorized last year's paper) and fails on new data.
- **Generalization** = doing well on new, unseen data. This is the real goal.
- **Underfitting** = the model learned too little; it is bad even on training data.

| Training score | Validation score | Meaning |
|---|---|---|
| 99% | 98% | Good, the model learned |
| 99% | 70% | Overfitting (big gap) |
| 60% | 58% | Underfitting |

### The 3 splits (in my words, corrected)

| Split | School example | Used for | Typical size |
|---|---|---|---|
| **Training** | Textbook + practice | The model learns from it (finds the weights). | ~70% |
| **Validation** | Mock test | Tuning: threshold, settings, choosing between models. Check its score as often as needed. | ~15% |
| **Test** | Final board exam | Only once, at the very end, to report the final score on new data. | ~15% |

### The golden rule of the test set

**Never use the test set to make decisions.** No tuning, no threshold choice, no model choice. If you look at the test score and go back to tune, the test set has "leaked" and its score can no longer be trusted (like seeing the board exam paper before the exam).

If the test score is bad: report it honestly. Do not tune on that same test set again. Get fresh test data, or redo the process with a new split.

### Q&A

**How long should I tune on validation?** Until one of these happens:

- the business target is met (for example recall ≥ 95%)
- the improvement becomes tiny (a few tries, almost no gain)
- time or budget runs out

Tuning on validation too many times can make the model memorize the validation set too. Cross-validation (Task 2) fixes this by checking on several different slices.

**New data keeps arriving. What about the test set?**

- One test set = used once per model version.
- A new model version gets a new, fresh test set (for example last month's orders).
- When the model is live, check its score on new data regularly: this is **monitoring**.
- With time-based data, always train on older data and test on newer data, so the test shows how the model does in the future.

| Months (RVO Steel example) | Use |
|---|---|
| Jan to Sep orders | Training + validation |
| Oct orders | Test set, used once |
| Nov orders | Monitoring the live model; if the score drops, build a new model and use Dec as its new test set |

### Day 12 note

On Day 12 the threshold 0.315 was chosen by looking at the test set. Strictly, that is test-set leakage: the threshold should be chosen on validation data, and the test set only used to report.

## Task 2: Cross-validation

Code: [`labs/d13-validation/cv.py`](../labs/d13-validation/cv.py)

- One validation split can be lucky or unlucky. **5-fold cross-validation** cuts the training data into 5 parts; each part is the validation set once, the other 4 train the model. You get 5 scores.
- The test set is never touched (only `X_train` goes into `cross_val_score`).

| Term | Meaning (my words) |
|---|---|
| **Mean** | Average of the 5 scores: how good the model typically is. |
| **Std** | How much the 5 scores differ from each other: how stable/reliable the score is. Small std = consistent. |

### Results (Day 12 model, 5 folds)

| Metric | Folds | Mean ± std |
|---|---|---|
| Accuracy | 0.967, 0.989, 0.956, 0.978, 0.967 | **0.971 ± 0.011** |
| Recall | 0.912, 1.000, 0.882, 0.971, 0.971 | **0.947 ± 0.043** |

### What I learned

- Day 12 showed recall 0.976 on one test split. Cross-validation shows the more honest picture: **0.947 ± 0.043**. Day 12's split was a bit lucky.
- Splitting did not create the variation. One split simply cannot show it; cross-validation reveals variation that was always there.
- Recall has a bigger std because each fold has only ~34 cancer patients, so one missed cancer moves recall by ~3%.

### What a large std means

**Mean tells how good the model is. Std tells how much we can trust that number.** A large std does not automatically mean a bad model; it means the score depends a lot on which data it sees. Common reasons:

| Reason | Meaning |
|---|---|
| Little data / small class | Each fold has few examples, so one mistake moves the score a lot |
| Unstable model | Small changes in data change the model a lot (a sign of overfitting) |
| Rare or unusual cases in one fold | One fold is harder than the others |

Fix: get more data, use a simpler model, and don't trust a single-split number.
