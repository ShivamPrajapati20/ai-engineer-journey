import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

df = pd.read_csv("../d07-pandas/data/telco.csv")
df["TotalCharges"] = pd.to_numeric(df["TotalCharges"], errors="coerce").fillna(0)

# 3 number columns, scaled (KMeans uses distance, so scaling matters: Day 13)
X = StandardScaler().fit_transform(df[["tenure", "MonthlyCharges", "TotalCharges"]])

ks, inertias, sils = range(2, 9), [], []
for k in ks:
    km = KMeans(n_clusters=k, n_init=10, random_state=42).fit(X)
    inertias.append(km.inertia_)
    sils.append(silhouette_score(X, km.labels_))
    print(f"k={k}  inertia={km.inertia_:>6,.0f}  silhouette={sils[-1]:.3f}")

fig, (a, b) = plt.subplots(1, 2, figsize=(10, 4))
a.plot(ks, inertias, "o-"); a.set_title("Elbow (lower = tighter)"); a.set_xlabel("k")
b.plot(ks, sils, "o-"); b.set_title("Silhouette (higher = cleaner)"); b.set_xlabel("k")
plt.tight_layout(); plt.savefig("k_choice.png")
print("Saved k_choice.png")