import matplotlib.pyplot as plt
import pandas as pd

WITH_ONLY_TRANSFORMED_BOTTOMS = True
WITH_NO_TRANSFORMED_BOTTOMS = False
WITH_NO_F_OUTLIER = True

df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5022).csv", sep=';'), "#5033 @ #5022"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", sep=';'), "#5033 @ #5023"
df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';'), "#5033 @ #5024"

categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'Total']
df["Total"] = df["G"] + df["C"] + df["A"]
df = df[categories].apply(pd.to_numeric, errors='coerce')


if WITH_NO_TRANSFORMED_BOTTOMS:
    df = df[df["A"] <= 20]
if WITH_ONLY_TRANSFORMED_BOTTOMS:
    df = df[df["A"] >= 20]
if WITH_NO_F_OUTLIER:
    df = df[df["F"] <= 150]
#df = df[df["C"] >= 225]


n = len(categories)
fig, axes = plt.subplots(n, n, figsize=(14, 12))

for i, cy in enumerate(categories):        # row    -> y axis
    for j, cx in enumerate(categories):    # column -> x axis
        ax = axes[i, j]

        if j < i:
            # lower triangle: scatter of cx (x) vs cy (y)
            pair = df[[cx, cy]].dropna()
            r = pair[cx].corr(pair[cy])
            ax.scatter(pair[cx], pair[cy], s=45, alpha=0.85,
                       edgecolor='k', c='tab:blue', zorder=3)
            ax.set_title(f"r = {r:.2f}", fontsize=9, pad=2)
            ax.grid(True, alpha=0.3)
        else:
            # diagonal + upper triangle: hide
            ax.axis('off')

        # label only the outer edges
        if j == 0:
            ax.set_ylabel(cy, fontsize=11, rotation=0, labelpad=15)
        if i == n - 1:
            ax.set_xlabel(cx, fontsize=11)
fig.suptitle(sample_nbr)
plt.tight_layout()
plt.show()