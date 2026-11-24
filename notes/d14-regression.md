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

## Task 3: Feature engineering

**Feature engineering** = building new columns from existing ones, to give the model a better clue.

### Pizza example

Pizza price depends on **area** = `length × width`. A linear model can only do `w1 × length + w2 × width + b`. It can add, but it cannot multiply. Give it an `Area` column and it gets the right clue directly.

### Results (validation RMSE)

Code: [`labs/d14-regression/features.py`](../labs/d14-regression/features.py)

| Feature | Formula | Before | After | Keep? |
|---|---|---|---|---|
| `HouseAge` | `YrSold - YearBuilt` | $36,840 | $36,840 | ❌ Dropped |
| `TotalSF` | `TotalBsmtSF + 1stFlrSF + 2ndFlrSF` | $36,840 | $36,840 | ❌ Dropped |
| `QualxSF` | `OverallQual × GrLivArea` | $36,840 | **$34,331** | ✅ Kept (-$2,509) |

### Why

- `HouseAge` and `TotalSF` are just **+ and −** of columns the model already has. A linear model can already build them by itself, so they add nothing new. The number did not move at all.
- `QualxSF` is a **multiplication**. A linear model cannot build it. It captures "big house **and** high quality = very expensive", which neither column says alone.

**Rule:** for a linear model, give it clues it cannot make by itself: products, ratios, logs. Sums and differences of existing columns don't help.

(Tree models are different: they can find interactions by themselves, but simple sums can still help them.)

## Task 4: Categorical features without blowing up

### Why text needs encoding

A model only does math on numbers. `"OldTown" × 0.5` means nothing, so text columns like `Neighborhood` were skipped until now.

| Way | Example | Problem |
|---|---|---|
| ❌ Label numbers | OldTown = 1, Edwards = 2, NoRidge = 3 | Model thinks NoRidge = 3 × OldTown. Names have no order. |
| ✅ One-hot | One 0/1 column per neighborhood | Each neighborhood gets its own bonus or penalty |

| House | is_OldTown | is_Edwards | is_NoRidge |
|---|---|---|---|
| A (OldTown) | 1 | 0 | 0 |
| B (NoRidge) | 0 | 0 | 1 |

### ColumnTransformer

Different columns need different steps. `ColumnTransformer` is the traffic police: number columns go to `SimpleImputer`, `Neighborhood` goes to `OneHotEncoder`. It sits inside the Pipeline, so it learns only from training rows.

```python
prep = ColumnTransformer([
    ("num", SimpleImputer(strategy="median"), num_cols),
    ("cat", OneHotEncoder(handle_unknown="ignore"), ["Neighborhood"]),
])
model = Pipeline([("prep", prep), ("model", LinearRegression())])
```

Code: [`labs/d14-regression/categorical.py`](../labs/d14-regression/categorical.py)

### Results

| | Train RMSE | Validation RMSE |
|---|---|---|
| Baseline (Task 1) | $33,918 | $36,840 |
| + `QualxSF` (Task 3) | | $34,331 |
| + `Neighborhood` one-hot (Task 4) | $30,104 | **$31,862** |

25 neighborhoods → 25 new 0/1 columns. Validation error dropped **$4,978 (13.5%)** from the baseline, with the same simple model. Gap is still small ($1,758), so no overfitting.

### Unseen category in production

| Setting | New neighborhood `"Mars"` |
|---|---|
| `OneHotEncoder()` | ❌ Crash: `ValueError: Found unknown categories ['Mars']` → API returns 500 |
| `OneHotEncoder(handle_unknown="ignore")` | ✅ All neighborhood columns = 0. No location bonus, the rest of the features still predict: **$165,800** |

**Catch:** `ignore` avoids the crash, but the guess for that house is worse (no location info) and it fails **silently**. In production, log and count unknown categories, and retrain when new ones show up often.

## Day 14 summary

Same `LinearRegression`, better inputs: **$36,840 → $31,862**. The win was in the features, not the model.
