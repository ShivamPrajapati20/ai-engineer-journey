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
