import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

df1 = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", sep=';') 
df2 = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';') 
data_center = [df1, df2]
num_categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
rng = np.random.default_rng(42)


fig, ax = plt.subplots(1, 2, figsize=(10, 6))

cx = "A"
cy = "C"
for axes, data in zip(ax.ravel(), data_center):
    data = data.dropna(subset=num_categories, how='all')
    for cat in num_categories:
        data[cat] = pd.to_numeric(data[cat], errors='coerce')

    data = data[data["Bottom"] == "Yes"]
    #data = data[data["C"] >= 220]

    pair = data[[cx, cy]].dropna()
    r = pair[cx].corr(pair[cy])
    axes.scatter(pair[cx], pair[cy], s=45, alpha=0.85,
            edgecolor='k', c='tab:blue', zorder=3)
    axes.set_title(f"r = {r:.2f}", fontsize=9, pad=2)
    axes.set_xlabel("A [nm]")
    axes.set_ylabel("C [nm]")
plt.show()