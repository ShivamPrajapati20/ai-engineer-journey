"""Day 13 Task 4: gradient descent with and without feature scaling.

100 fake houses: price (in $1000s) = 0.15*size + 20*beds + 50 + noise.
size is 500-3000, beds is 1-5, so the two features have very different ranges.
"""
import numpy as np

rng = np.random.default_rng(0)
size = rng.uniform(500, 3000, 100)
beds = rng.integers(1, 6, 100).astype(float)
y = 0.15 * size + 20 * beds + 50 + rng.normal(0, 10, 100)
X = np.column_stack([size, beds])


def gradient_descent(X, y, alpha, max_iter=100_000, tol=1e-6):
    w = np.zeros(X.shape[1])
    b = 0.0
    prev = None
    for i in range(1, max_iter + 1):
        err = X @ w + b - y                  # vectorized prediction error
        cost = (err ** 2).mean() / 2
        if not np.isfinite(cost):
            return i, "blew up"
        if prev is not None and abs(prev - cost) < tol:   # convergence check
            return i, f"converged, cost={cost:.2f}"
        prev = cost
        w -= alpha * (X.T @ err) / len(y)
        b -= alpha * err.mean()
    return max_iter, "NOT converged"


with np.errstate(over="ignore", invalid="ignore"):
    print("RAW features")
    for a in [1e-7, 1e-6, 1e-5]:
        print(f"  alpha={a:<8} ->", gradient_descent(X, y, a))

    X_scaled = (X - X.mean(axis=0)) / X.std(axis=0)   # z-score scaling
    print("SCALED features")
    for a in [0.01, 0.1, 0.5, 1.5, 2.5]:
        print(f"  alpha={a:<8} ->", gradient_descent(X_scaled, y, a))
