import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data5031 = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5031 @ #5024).csv", sep=';')
data5033 = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';')
data5034 = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5034 @ #5024).csv", sep=';')


categories = ["Bottom", "Top", "Nanocluster?", "Au particle?"]
x_axes_cat = {"550C (#5034 @ #5024)": data5034, "575C (#5031 @ #5024)": data5031, "625C (#5033 @ #5024)": data5033}
bar_colors = {"550C (#5034 @ #5024)": "tab:purple","575C (#5031 @ #5024)": "tab:blue", "625C (#5033 @ #5024)": "tab:red"}

fig, ax = plt.subplots(figsize=(9, 6))

n_groups = len(x_axes_cat)
width = 0.8 / n_groups                       # bars share each category slot
x = np.arange(len(categories))

for i, (sec, data) in enumerate(x_axes_cat.items()):
    procentages = []
    for cat in categories:
        col = data[cat]
        yes = (col == "Yes").sum()
        answered = col.isin(["Yes", "No", "?"]).sum()     # ignore blanks and "?"
        procentages.append(yes / answered * 100 if answered else 0)

    offset = (i - (n_groups - 1) / 2) * width
    bars = ax.bar(x + offset, procentages, width=width, label=sec,
                  color=bar_colors[sec], edgecolor="k", alpha=0.85)
    ax.bar_label(bars, fmt="%.0f%%", padding=2, fontsize=9)

ax.set_xticks(x)
ax.set_xticklabels(["Transformed bottom", "Not headless", "Nanocluster?", "Au particle?"])
ax.set_ylabel("Percentage 'Yes' [%]")
ax.set_ylim(0, 105)
ax.set_title("Percentage 'Yes' by growth temperature")
ax.legend(title="Growth temperature")
ax.grid(True, axis="y", alpha=0.3)
plt.tight_layout()
plt.show()