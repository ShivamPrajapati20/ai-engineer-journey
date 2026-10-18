# Day 07 — EDA: Telco Customer Churn

Dataset: [Kaggle Telco Customer Churn](https://www.kaggle.com/datasets/blastchar/telco-customer-churn) — 7,043 customers, 21 columns. Overall churn: **26.5%**.
Script: [`labs/d07-pandas/explore.py`](../labs/d07-pandas/explore.py)

## First look
- Shape: 7,043 rows × 21 columns.
- `isna().sum()` reports **0 nulls** — but `TotalCharges` loads as text, which hides bad values.

## Cleaning
- `TotalCharges` had **11 blank strings (`" "`)**, invisible to `isna()`.
- All 11 are customers with **tenure = 0** (not billed yet), so the true value is **0**.
- Converted with `pd.to_numeric(errors="coerce")`, then `fillna(0)`. Kept all 7,043 rows.
- Rejected: dropping (loses real customers, all 11 are `Churn = No`) and mean/median fill (would invent ~$1,400–2,300 of charges for people billed nothing).
- Result: `TotalCharges` is float64 with 0 NaN.

## Churn by Contract
| Contract | Churn rate | Customers |
|---|---:|---:|
| Month-to-month | 42.7% | 3,875 |
| One year | 11.3% | 1,473 |
| Two year | 2.8% | 1,695 |

## Churn by InternetService
| InternetService | Churn rate | Customers |
|---|---:|---:|
| Fiber optic | 41.9% | 3,096 |
| DSL | 19.0% | 2,421 |
| No | 7.4% | 1,526 |

## Churn by tenure (months)
| Tenure | Churn rate | Customers |
|---|---:|---:|
| 0–12 | **47.4%** | 2,186 |
| 13–24 | 28.7% | 1,024 |
| 25–48 | 20.4% | 1,594 |
| 49+ | 9.5% | 2,239 |

**Highest-churn segment:** customers in their first 12 months — **47.4%**, almost double the 26.5% baseline.
Combined, month-to-month customers in their first 12 months churn at **51.4%**.

## Hypothesis
Churn is driven by **low commitment early in the relationship**: new customers on month-to-month contracts have nothing keeping them, and they leave before they have used the service long enough to stay. Fiber customers churn about twice as much as DSL, possibly because fiber costs more — to test, compare `MonthlyCharges` between churned and retained fiber customers.

**How to test the main hypothesis:** offer first-year month-to-month customers a discounted 1-year contract and compare their 12-month churn with a control group.

*These tables show correlation, not causation.*
