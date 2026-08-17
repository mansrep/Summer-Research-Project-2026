import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

num_data, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5022).csv", sep=';'), "#5033 @ #5022"
num_data, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", sep=';'), "#5033 @ #5023"
num_data, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';'), "#5033 @ #5024"
num_categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

num_data = num_data.dropna(subset=num_categories, how='all') #"All" make so that dropna drops a row only if every value is missing
for cat in num_categories:
    num_data[cat] = pd.to_numeric(num_data[cat], errors='coerce')

markers = {"Yes": '^', "No": 'o', "?": "s"}
colours = {"Yes": "tab:green", "No": "tab:purple", "?": "gray"}
edge = {"Yes": "black", "No": "orange", "?": "gray"}

fig, ax = plt.subplots(figsize=(9,6))
seen = set()

for xpos, cat in enumerate(num_categories):
    sub = num_data[[cat, 'Nanocluster?', 'Top', 'Bottom']].dropna(subset=[cat])
    for nano in markers:
        for top in colours:
            for bottom in edge:
                rows = sub[(sub["Nanocluster?"] == nano) & (sub["Top"] == top) & (sub["Bottom"] == bottom)]
                if len(rows) == 0:
                    continue
                label = f"Nanocluster?: {nano}, Transformed top: {top}, Transformed bottom: {bottom}"
                jitter = rng.uniform(-0.01, 0.01, size=len(rows))
                ax.scatter(np.full(len(rows), xpos + jitter), rows[cat].values, s=110, alpha=0.85, zorder=3, linewidths=2.2, c=colours[top],
                           marker=markers[nano], edgecolors=edge[bottom], 
                           label=label if label not in seen else None)
                seen.add(label)

    vals = sub[cat].values    
    mean = vals.mean()
    SD = vals.std(ddof=1)
    ax.errorbar(xpos + 0.14, mean, yerr=SD, fmt='o', color='black',
                capsize=5, markersize=8, zorder=4)
    #print(mean)
    
ax.set_xticks(range(len(num_categories)))
ax.set_xticklabels(num_categories)
ax.set_xlabel("Dimension")
ax.set_ylabel("[nm]")
ax.set_title("Measurements by category")
ax.grid(True, axis='y', alpha=0.3)
ax.legend(loc="upper left")
fig.suptitle(sample_nbr)
plt.tight_layout()
plt.show()