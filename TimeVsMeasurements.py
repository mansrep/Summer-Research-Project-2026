import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

rng = np.random.default_rng(42)

data5022, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5022).csv", sep=';'), "#5033 @ #5022"
data5023, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", sep=';'), "#5033 @ #5023"
data5024, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';'), "#5033 @ #5024"
num_categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G']

data5022 = data5022.dropna(subset=num_categories, how="all")
data5023 = data5023.dropna(subset=num_categories, how='all') #"All" make so that dropna drops a row only if every value is missing
data5024 = data5024.dropna(subset=num_categories, how='all') #"All" make so that dropna drops a row only if every value is missing

for cat in num_categories:
    data5022[cat] = pd.to_numeric(data5022[cat], errors="coerce")
    data5023[cat] = pd.to_numeric(data5023[cat], errors='coerce')
    data5024[cat] = pd.to_numeric(data5024[cat], errors="coerce")

data5022 = data5022[data5022["Bottom"] == "Yes"]
data5023 = data5023[data5023["Bottom"] == "Yes"]
data5024 = data5024[data5024["Bottom"] == "Yes"]
#data5024 = data5024[data5024["C"] >= 150]

fig, ax = plt.subplots(figsize=(9,6))
seen = set()
for xpos, cat in enumerate(num_categories):
    vals22 = data5022[cat].dropna().values
    vals23 = data5023[cat].dropna().values
    vals24 = data5024[cat].dropna().values
    jitter22 = rng.uniform(-0.01, 0.01, size=len(vals22))
    jitter23 = rng.uniform(-0.01, 0.01, size=len(vals23))
    jitter24 = rng.uniform(-0.01, 0.01, size=len(vals24))
    label22 = "5s (#5033 @ #5022)"
    label23 = "10s (#5033 @ #5023)"
    label24 = "15s (#5033 @ #5024)"
    ax.scatter(np.full(len(vals22), xpos + jitter22), vals22, s=110, alpha=0.85, zorder=3, c = "purple", label=label22 if label22 not in seen else None)
    ax.scatter(np.full(len(vals23), xpos + jitter23), vals23, s=110, alpha=0.85, zorder=3, c = "blue", label=label23 if label23 not in seen else None)
    ax.scatter(np.full(len(vals24), xpos + jitter24), vals24, s=110, alpha=0.85, zorder=3, c = "red", label=label24 if label24 not in seen else None)
    seen.add(label22)
    seen.add(label23)
    seen.add(label24)
    mean22 = vals22.mean()
    mean23 = vals23.mean()
    mean24 = vals24.mean()
    SD22 = vals22.std(ddof=1)
    SD23 = vals23.std(ddof=1)
    SD24 = vals24.std(ddof=1)
    ax.errorbar(xpos + 0.10, mean22, yerr=SD22, fmt='o', color="purple", 
                capsize=5, markersize=8, zorder=4)
    ax.annotate(f"{mean22:.1f}", (xpos + 0.10, mean22), 
                            textcoords="offset points", xytext=(8, 0),
                            va="center", fontsize=8, color="purple")
    ax.errorbar(xpos + 0.13, mean23, yerr=SD23, fmt='o', color='blue',
                capsize=5, markersize=8, zorder=4)   
    ax.annotate(f"{mean23:.1f}", (xpos + 0.13, mean23),
                            textcoords="offset points", xytext=(8, 0),
                            va='center', fontsize=8, color="blue") 
    ax.errorbar(xpos + 0.16, mean24, yerr=SD24, fmt='o', color='red',
                capsize=5, markersize=8, zorder=4)
    ax.annotate(f"{mean24:.1f}", (xpos + 0.16, mean24),
                            textcoords="offset points", xytext=(8, 0),
                            va='center', fontsize=8, color="red") 
ax.set_xticks(range(len(num_categories)))
ax.set_xticklabels(num_categories)
ax.set_xlabel("Dimension")
ax.set_ylabel("[nm]")
ax.set_title("Measurements by category")
ax.grid(True, axis='y', alpha=0.3)
ax.legend(loc="upper right")
plt.tight_layout()
plt.show()
    