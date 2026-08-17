import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

REMOVE_OUTLIERS = False
F_CUTOFF = 1500
B_CUTOFF = 1500
C_CUTOFF = 1500

df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5022).csv", sep=';'), "#5033 @ #5022"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", sep=';'), "#5033 @ #5023"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';'), "#5033 @ #5024"
categories = ['B','C','F', 'G']

fig, axes = plt.subplots(1, 3, figsize=(15, 8))

for ax, cat in zip(axes.ravel(), categories):
    sub = df[[cat, "Bottom"]].dropna(subset=[cat])
    Yes_values = sub.loc[sub["Bottom"] == "Yes", cat].values
    No_values = sub.loc[sub["Bottom"] == "No", cat].values
    
    if REMOVE_OUTLIERS:
        if cat == "F":
            Yes_values = Yes_values[Yes_values <= F_CUTOFF]
            No_values = No_values[No_values <= F_CUTOFF]
        elif cat == "B":
            Yes_values = Yes_values[Yes_values <= B_CUTOFF]
            No_values = No_values[No_values <= B_CUTOFF]
        elif cat == "C":
            Yes_values = Yes_values[Yes_values <= C_CUTOFF]
            No_values = No_values[No_values <= C_CUTOFF]

    ax.hist(Yes_values, bins=np.histogram_bin_edges(Yes_values, bins='doane'), density=True, alpha=0.4, color='blue', edgecolor='k', label=f"Bottom=Yes (n={len(Yes_values)})")
    ax.hist(No_values, bins=np.histogram_bin_edges(No_values, bins='doane'), density=True, alpha=0.4, color='yellow', edgecolor='k', label=f"Bottom=No (n={len(No_values)})")    
    ax.set_title(f"Category {cat}")
    ax.set_xlabel("[nm]")
    ax.set_ylabel("Density")
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)

fig.suptitle(sample_nbr)
plt.tight_layout()
plt.show()