import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)
data5031, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5031 @ #5024).csv", sep=';'), "#5031 @ #5024"
data5033, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';'), "#5033 @ #5024"
data5034, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5034 @ #5024).csv", sep=';'), "#5034 @ #5024"

num_categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

data5031 = data5031.dropna(subset=num_categories, how="all")
data5033 = data5033.dropna(subset=num_categories, how='all') #"All" make so that dropna drops a row only if every value is missing
data5034 = data5034.dropna(subset=num_categories, how='all') #"All" make so that dropna drops a row only if every value is missing

for cat in num_categories:
    data5031[cat] = pd.to_numeric(data5031[cat], errors="coerce")
    data5033[cat] = pd.to_numeric(data5033[cat], errors='coerce')
    data5034[cat] = pd.to_numeric(data5034[cat], errors="coerce")

data5031 = data5031[data5031["Bottom"] == "Yes"]
data5033 = data5033[data5033["Bottom"] == "Yes"]
data5034 = data5034[data5034["Bottom"] == "Yes"]

fig, ax = plt.subplots(figsize=(9,6))
seen = set()
for xpos, cat in enumerate(num_categories):
    vals31 = data5031[cat].dropna().values
    vals33 = data5033[cat].dropna().values
    vals34 = data5034[cat].dropna().values
    jitter31 = rng.uniform(-0.01, 0.01, size=len(vals31))
    jitter33 = rng.uniform(-0.01, 0.01, size=len(vals33))
    jitter34 = rng.uniform(-0.01, 0.01, size=len(vals34))
    label34 = "550C (#5034 @ #5024)"
    label31 = "575C (#5031 @ #5024)"
    label33 = "625C (#5033 @ #5024)"
    ax.scatter(np.full(len(vals34), xpos + jitter34), vals34, s=110, alpha=0.85, zorder=3, c = "red", label=label34 if label34 not in seen else None)
    ax.scatter(np.full(len(vals31), xpos + jitter31), vals31, s=110, alpha=0.85, zorder=3, c = "purple", label=label31 if label31 not in seen else None)
    ax.scatter(np.full(len(vals33), xpos + jitter33), vals33, s=110, alpha=0.85, zorder=3, c = "blue", label=label33 if label33 not in seen else None)
    seen.add(label31)
    seen.add(label33)
    seen.add(label34)
    mean31 = vals31.mean()
    mean33 = vals33.mean()
    mean34 = vals34.mean()
    SD31 = vals31.std(ddof=1)
    SD33 = vals33.std(ddof=1)
    SD34 = vals34.std(ddof=1)
    ax.errorbar(xpos + 0.09, mean34, yerr=SD34, fmt='o', color='red',
                capsize=5, markersize=8, zorder=4)
    ax.annotate(f"{mean34:.1f}", (xpos + 0.09, mean34),
                            textcoords="offset points", xytext=(8, 0),
                            va='center', fontsize=8, color="red") 
    ax.errorbar(xpos + 0.06, mean31, yerr=SD31, fmt='o', color="purple", 
                capsize=5, markersize=8, zorder=4)
    ax.annotate(f"{mean31:.1f}", (xpos + 0.06, mean31), 
                            textcoords="offset points", xytext=(8, 0),
                            va="center", fontsize=8, color="purple")
    ax.errorbar(xpos + 0.03, mean33, yerr=SD33, fmt='o', color='blue',
                capsize=5, markersize=8, zorder=4)   
    ax.annotate(f"{mean33:.1f}", (xpos + 0.03, mean33),
                            textcoords="offset points", xytext=(8, 0),
                            va='center', fontsize=8, color="blue") 
    
ax.set_xticks(range(len(num_categories)))
ax.set_xticklabels(num_categories)
ax.set_xlabel("Dimension")
ax.set_ylabel("[nm]")
ax.set_title("Measurements by category")
ax.grid(True, axis='y', alpha=0.3)
ax.legend(loc="upper right")
plt.tight_layout()
plt.show()
    