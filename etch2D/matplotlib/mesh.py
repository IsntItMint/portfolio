import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from Fileinfo import Fileinfo
# Load the uploaded CSV files for mesh coordinates


def skip_with_last(arr, step):
    indices = list(range(0, len(arr), step))
    if indices[-1] != len(arr) - 1:
        indices.append(len(arr) - 1)
    return indices


x_path = "./x.csv"
y_path = "./y.csv"

# Create mesh grid for plotting
x_values_mm = pd.read_csv(x_path, header=None).values.flatten() * 1e+3
y_values_mm = pd.read_csv(y_path, header=None).values.flatten() * 1e+3
X_mm, Y_mm = np.meshgrid(x_values_mm, y_values_mm)

# Apply skip rule to both axes
skip_x = 5
skip_y = 5
skip_x_indices = skip_with_last(x_values_mm, skip_x)
skip_y_indices = skip_with_last(y_values_mm, skip_y)
X_sub = X_mm[np.ix_(skip_y_indices, skip_x_indices)]
Y_sub = Y_mm[np.ix_(skip_y_indices, skip_x_indices)]


# Plot the computational mesh
with plt.style.context(Fileinfo.context):
    plt.figure(figsize=(3.25, 1.21875))
    plt.plot(X_sub, Y_sub, color="gray", linewidth=0.5)      # horizontal lines
    plt.plot(X_sub.T, Y_sub.T, color="gray", linewidth=0.5)  # vertical lines
    plt.xlabel("x [mm]")
    plt.ylabel("y [mm]")
    plt.xlim(0, 100.0)
    plt.ylim(0, 1.0)
    # plt.title("Computational Mesh for Flow Cell Simulation")
    plt.grid(False)
    plt.tight_layout()
    plt.savefig("./mesh.pdf", bbox_inches='tight')
