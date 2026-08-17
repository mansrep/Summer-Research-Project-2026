import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';'), "#5033 @ #5024"
num_categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

for cat in num_categories:
    data[cat] = pd.to_numeric(data[cat], errors='coerce')

data = data[data["Bottom"] == "No"]

segment = "G"          # <-- which segment's length to show on the y-axis; change to B, C, ...

# three G bands: (label, low, high inclusive, color)
bands = [
    ("520–500", 500, 520, "tab:red"),
    ("475–455", 455, 475, "tab:green"),
    ("441–425", 425, 441, "tab:blue"),
]

def which_band(g):
    for name, lo, hi, _ in bands:
        if pd.notna(g) and lo <= g <= hi:
            return name
    return None

data = data.copy()
data["Gband"] = data["G"].apply(which_band)
data = data[data["Gband"].notna()]            # drop wires whose G is outside all bands
data = data.dropna(subset=[segment])          # need the segment value to plot it
data = data.sort_values(["Gband", segment]).reset_index(drop=True)

xpos = np.arange(len(data))
fig, ax = plt.subplots(figsize=(10, 6))

for name, lo, hi, color in bands:
    mask = (data["Gband"] == name).values
    ax.scatter(xpos[mask], data[segment].values[mask], s=110, alpha=0.85,
               edgecolor='k', c=color, zorder=3, label=f"G {name} nm")

ax.set_xticks(xpos)
ax.set_xticklabels(data["wire #"].astype(str).values)
ax.set_xlabel("Wire #")
ax.set_ylabel(f"{segment} length [nm]")
ax.set_title(f"Segment {segment} length by wire, grouped by G-band (Bottom=No)")
ax.grid(True, axis='y', alpha=0.3)
ax.legend(title="G length band")
fig.suptitle(sample_nbr)
plt.tight_layout()
plt.show()