import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================== SETTINGS ====================
CSV_PATH   = "MnAs_GaAs_summer_project_sample_overview1(#5031 @ #5024).csv"
SAMPLE_NBR = "#5033 @ #5024"
# =================================================

df = pd.read_csv(CSV_PATH, sep=';')
df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
for col in ['A', 'C', 'G']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

df = df[df["Bottom"] == "Yes"]
df = df.dropna(subset=["A", "C", "G"])
# wire id
wire_col = next((c for c in df.columns if 'wire' in c.lower()), None)
labels = df[wire_col].astype(str).values if wire_col else np.arange(len(df)).astype(str)
all_Au_tot_lengths = []
all_No_tot_lengts = []

# ==================== PLOT ====================
x = np.arange(len(df))
fig, ax = plt.subplots(figsize=(12, 6))
for i, (index, row) in enumerate(df.iterrows()):
    tot_length = row["G"] + row["A"] + row["C"]
    """ if tot_length < 650:
        continue """
    if row["Au particle?"] == "Yes":
        color = "gold"
        all_Au_tot_lengths.append(tot_length)
    else:
        color = "dimgrey"
        all_No_tot_lengts.append(tot_length)
    ax.scatter(i, tot_length, s=70, color=color, edgecolor='k', zorder=3)
    

mean_Au = np.mean(all_Au_tot_lengths)
mean_No = np.mean(all_No_tot_lengts)

ax.axhline(mean_Au,   color='gold',   ls='--', lw=2, zorder=2,
           label=f'mean = {mean_Au:.2f}')
ax.axhline(mean_No, color='dimgrey', ls='-.', lw=2, zorder=2,
           label=f'mean = {mean_No:.2f}')

ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=90, fontsize=7)
ax.set_xlabel("Wire #")
ax.set_ylabel("Length [nm]")
ax.set_title(f"Per wire total length — {SAMPLE_NBR}")
ax.grid(True, axis='y', alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()