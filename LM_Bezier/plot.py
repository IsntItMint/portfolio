import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from LM import bezier


df = pd.read_csv("data/points.csv")
x = df.iloc[:, 0].values
y = df.iloc[:, 1].values

for n in range(3, 21):
    ctrl_df = pd.read_csv(f"result/ctrl_n{n}.csv")
    Px = ctrl_df["Px"].values
    Py = ctrl_df["Py"].values

    t_vals = np.linspace(0, 1, 200)
    Bx, By = zip(*map(lambda t: bezier(t, Px, Py, n), t_vals))

    plt.figure(figsize=(6, 6))
    plt.plot(x, y, 'o', label='data points')
    plt.plot(Bx, By, '-', label='Bézier curve')
    plt.xlabel("x")
    plt.ylabel("y")
    plt.title(f"Bézier Fit with {n} Control Points")
    plt.legend()
    plt.axis("equal")
    plt.grid(True)
    plt.savefig(f"fig/plot_n{n}.png")
    plt.close("all")
