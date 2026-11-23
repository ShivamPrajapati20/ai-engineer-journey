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

## Task 3: Prevent leakage with a Pipeline

Code: [`labs/d13-validation/leakage.py`](../labs/d13-validation/leakage.py)

### Leakage (my words)

When we validate a model, we must never show it the test/validation data. Leakage is getting a "peek" at the answers before the test. The score then looks good, but the model is not really that good on new data. Leakage makes a model **look** better, not **be** better.

### Where it happens with scaling

| Way | What happens |
|---|---|
| **Naive** (leaky) | `StandardScaler` is fit on all training rows first, then cross-validation runs. The scaler has already seen each fold's validation rows (their average and spread). |
| **Pipeline** (correct) | `Pipeline([("scaler", StandardScaler()), ("clf", LogisticRegression())])`. In every fold the scaler is fit only on that fold's training part; the validation part stays unseen. |

**Pipeline (my words):** a box that keeps the scaler and the model together and keeps the validation data secret, so nothing leaks.

### Results (recall, 5 folds)

| Version | Recall |
|---|---|
| Naive | 0.9471 ± 0.0432 |
| Pipeline | 0.9471 ± 0.0432 |

They are the same here: scaling only learns the average and spread of each column, and with 455 rows these barely change when one fold is included or not. The leak is real but too small to move the score.

### When the leak is big

Demo: 5,000 random columns and random labels (nothing to learn, true score = 50%), with a "pick the best 20 columns" step:

| Version | Score | Truth |
|---|---|---|
| Naive (columns picked on all data) | 78.5% | Fake: column picking saw the validation answers |
| Pipeline (columns picked inside each fold) | 49.5% | Honest: random data = coin flip |

### Rule

Every step that **learns from data** (scaling, feature selection, filling missing values, encoding) goes **inside the Pipeline**, so it learns only from each fold's training part.

## Task 4: Multiple features, vectorization, feature scaling, learning rate

### Multiple features

```
price = w1 × size + w2 × beds + w3 × age + b
```

Each weight = how much the price changes when that one feature goes up by 1 and everything else stays the same.

### Vectorization

```python
pred = X @ w + b      # all rows at once, no Python loop
```

NumPy runs this in C over all rows together, so it is 10 to 100 times faster than a loop.

### Gradient descent in one line

Standing on a hill in fog: feel the slope, take a small step downhill, repeat. Height = cost, position = weights, step size = learning rate `alpha`.

### Feature scaling

| Feature | Range |
|---|---|
| size | 500 to 3000 |
| beds | 1 to 5 |

- There is **one** step size for all weights.
- A tiny change in `w_size` moves the prediction a lot (it is multiplied by up to 3000). `w_beds` needs a big change to matter.
- The cost surface becomes a **long, narrow valley**. A step big enough for `beds` overshoots on `size` and blows up. A step small enough for `size` makes `beds` crawl.
- **Z-score scaling:** `z = (x - mean) / std` puts every feature around -2 to +2. The valley becomes a **round bowl**, and the slope points straight to the bottom, so bigger steps are safe.

### Experiment ([`labs/d13-validation/scaling_gd.py`](../labs/d13-validation/scaling_gd.py))

| Data | alpha | Result |
|---|---|---|
| Raw | 0.0000001 | Not converged after 100,000 steps |
| Raw | 0.000001 | Blew up at step 310 |
| Raw | 0.00001 | Blew up at step 96 |
| Scaled | 0.01 | Converged in 1058 steps |
| Scaled | 0.1 | Converged in 114 steps |
| Scaled | **0.5** | **Converged in 20 steps** |
| Scaled | 2.5 | Blew up |

No alpha worked on raw data. On scaled data, 20 steps were enough.

### Learning rate

| alpha | Effect |
|---|---|
| Too small | Right direction, very slow |
| Good | Reaches the bottom fast |
| Too big | Overshoots, cost goes up, then explodes |

Try a ladder about 3x apart: `0.001, 0.003, 0.01, 0.03, 0.1, 0.3, 1`. Pick the largest one where the cost still goes down every step.

### Checking convergence

Plot cost vs iterations (learning curve).

| Curve | Meaning |
|---|---|
| Goes down every step, then flattens | Converged |
| Goes **up** at any point | alpha too big (or a bug) |
| Falls very slowly | Increase alpha |

Automatic check: stop when the cost drops by less than a tiny number (for example `0.000001`) in one step.

### Answers

1. **Why does scaling speed up gradient descent?** All features get the same range, so the cost surface turns from a long narrow valley into a round bowl. One learning rate now fits every weight, the slope points straight to the minimum, and we can take bigger steps without blowing up.
2. **Cost goes up during training?** The learning rate is too big (overshooting), or there is a bug. Lower alpha (about 3x) and check the code.
3. **Why fit the scaler only on train data?** The mean and std must not include validation or test rows, or their information leaks into training (Task 3). Fit on train, then only `transform` validation and test. A `Pipeline` does this for you.

### When scaling matters

| Needs scaling | Does not need it |
|---|---|
| Gradient descent models (logistic regression, SGD, neural networks) | Tree models (decision tree, random forest, XGBoost) |
| Distance models (KNN, SVM) | They only check "is this value above a threshold?" |
