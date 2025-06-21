import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv("result/AIC.csv")
n = df.iloc[:, 0].values
AIC = df.iloc[:, 1].values

plt.figure(figsize=(6, 6))
plt.plot(n, AIC, 'o-')

plt.xticks(np.arange(min(n), max(n)+1, 1))
plt.xlabel("control points")
plt.ylabel("AIC")
plt.yscale("log")
plt.title("Model Selection using AIC in Bézier Curve Fitting")
plt.grid(True)
plt.savefig("fig/AIC.png")
plt.close('all')
