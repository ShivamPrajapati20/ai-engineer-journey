# Day 11: What ML is + supervised learning

## Task 1: Linear regression (model, loss, fit)

### The model

```
y = w × x + b
```

### The 5 terms (in my own words)

| Term | My definition | Taxi example |
|---|---|---|
| **Feature** (x) | The input we give the model. | Miles driven |
| **Label** (y) | The output we want the model to predict. | Fare |
| **Weight** (w) | How much the prediction changes for each 1 unit of a feature. It can also be negative (the prediction goes down). | $2 per mile |
| **Bias** (b) | The initial value: the prediction when every feature is 0. | $3 starting fee |
| **Loss** | The difference between the actual value and the prediction, averaged over all examples. Smaller loss means a better model. | Predicted $20, actual $23 → error of $3 |

```
fare = 2 × miles + 3
```

| Miles | Fare |
|---|---|
| 0 | $3 (only the bias) |
| 1 | $5 |
| 10 | $23 |

### How a model learns (training / fitting)

1. Start with random weight and bias.
2. Predict the label for every example.
3. Measure the loss.
4. Adjust weight and bias a little to make the loss smaller.
5. Repeat until the loss stops going down.

The model does not "understand" taxis. It only finds the numbers (w, b) that make the loss smallest.

### Two common losses

| Loss | Formula | Effect |
|---|---|---|
| **MAE** (Mean Absolute Error) | average of \|actual − predicted\| | All errors count the same |
| **MSE** (Mean Squared Error) | average of (actual − predicted)² | Big errors are punished much more |

Example with errors 2 and 10: MAE = 6, MSE = 52.

### Link to earlier days

| ML word | Seen before as |
|---|---|
| Features | DataFrame columns (Day 7) |
| Label | The `Churn` column (Day 7) |
| Prediction | `x @ w + b`, a dot product (Day 6) |

## Task 4: Classification vs regression

| Type | Answer is | Question style |
|---|---|---|
| **Regression** | a number | How much? How many? How long? |
| **Classification** | a category | Which one? Yes or no? |

Quick test: can you average two answers and still get a valid answer? 5 and 7 days → 6 days (regression). "Accepted" and "rejected" → no average (classification).

### Logistic regression

1. Compute `w·x + b` (same as linear regression).
2. Squeeze it into 0 to 1 with the **sigmoid** function → a **probability**.
3. Above 0.5 → "yes", below → "no".

Despite the name, logistic regression is used for **classification**.

### 3 problems from my work (RVO Steel)

| # | Problem | Type | Target |
|---|---|---|---|
| 1 | How long will this order take to finish? | Regression | `lead_time_days` |
| 2 | Does the mill test report (MTR) match the spec? | Classification | `mtr_matches_spec` (yes/no) |
| 3 | Will this order ship late? | Classification | `ships_late` (yes/no) |

**Note on #2:** matching an MTR to a spec is usually a **rule check** (each value inside the spec range), so plain `if` checks beat ML: faster, 100% accurate, easy to explain. ML only helps when the rules are fuzzy or unknown, for example learning which MTRs reviewers rejected in the past even when the numbers passed.

**Same data, different question:** "how many days?" is regression; "will it be late?" is classification.
