# Day 14: Regression & feature engineering

Focus: often the win is in the features, not the model.

## Task 1 + 2: Hyperparameters and an honest RMSE

### Parameters vs hyperparameters

| | Who sets it | Examples |
|---|---|---|
| **Parameter** | The model learns it | weights, bias |
| **Hyperparameter** | I set it before training | learning rate, batch size, epochs |

| Hyperparameter | Meaning |
|---|---|
| **Learning rate** | Size of each step downhill |
| **Batch size** | Rows seen before one weight update (1 = SGD, all = full batch, 32 to 512 = mini-batch) |
| **Epoch** | One full pass over all training rows |

1000 rows, batch size 100 → 10 updates per epoch. Too many epochs → overfitting: validation loss goes up while training loss keeps going down.

### RMSE

```
RMSE = sqrt( mean( (actual - predicted)² ) )
```

Same unit as the target (dollars). Big errors are punished more.

### Setup

- Data: Kaggle House Prices, `train.csv` only (1460 houses). Not committed (`labs/*/data/` is git-ignored).
- 36 numeric features, `Id` and `SalePrice` dropped.
- 80/20 train/validation split, `random_state=42` so the split is the same every run.
- Pipeline: `SimpleImputer(strategy="median")` → `LinearRegression()`. The imputer learns medians, so it lives inside the Pipeline (Day 13 rule).

Code: [`labs/d14-regression/train.py`](../labs/d14-regression/train.py)

### Result (baseline)

| | RMSE |
|---|---|
| Train | $33,918 |
| Validation | **$36,840** |
| Gap | $2,922 |

### What it means

- **Small gap (about 8%)** → not overfitting. The model does about as well on unseen houses as on seen ones.
- **But the error itself is big:** average `SalePrice` is about $181,000, so $36,840 is about 20% off on a typical house.
- Small gap + big error = **underfitting**. The model is too simple for the data: a straight-line model, and 43 text columns (like `Neighborhood`) are not used yet.
- Fix is better features (Task 3) and categorical columns (Task 4), not a fancier model.

### Bugs I hit

| Bug | Fix |
|---|---|
| `X = df...drop(..., inplace=True)` → `X` was `None` | `inplace=True` returns nothing. Drop `inplace` and save the result. |
| `train_test_split` not imported | `from sklearn.model_selection import train_test_split` |
| Named the 20% part `X_test` | It is used for decisions, so it is **validation** (`X_val`) |
