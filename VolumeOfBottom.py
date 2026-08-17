"""
Volume ratio (bottom/top) per nanowire.
Top volume    = cylinder with length A, diameter B  ->  pi*(B/2)^2 * A
Bottom volume = cylinder with length D, diameter E  ->  pi*(E/2)^2 * D
Ratio = bottom / top
Plots each wire's ratio with mean and median lines.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ==================== SETTINGS ====================
CSV_PATH   = "MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv"
SAMPLE_NBR = "#5033 @ #5024"
# =================================================

df = pd.read_csv(CSV_PATH, sep=';')
df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
for col in ['A', 'B', 'D', 'E']:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# need all four measurements to form the ratio
df = df.dropna(subset=['A', 'B', 'D', 'E']).copy()
df = df[df["Bottom"] == "Yes"]

# cylinder volumes (pi and 1/4 cancel in the ratio, but computed fully for clarity)
df['V_bottom']    = np.pi * (df['B'] / 2)**2 * df['A']

# wire id
wire_col = next((c for c in df.columns if 'wire' in c.lower()), None)
labels = df[wire_col].astype(str).values if wire_col else np.arange(len(df)).astype(str)

bottom_v = df["V_bottom"].values
mean = bottom_v.mean()
median = np.median(bottom_v)

print(f"n wires: {len(df)}")
print(f"mean volume:   {mean:.3f}")
print(f"median volume: {median:.3f}")

# ==================== PLOT ====================
x = np.arange(len(df))
fig, ax = plt.subplots(figsize=(12, 6))
ax.scatter(x, bottom_v, s=70, color='tab:blue', edgecolor='k', zorder=3)

ax.axhline(mean,   color='tab:red',   ls='--', lw=2, zorder=2,
           label=f'mean = {mean:.2f}')
ax.axhline(median, color='tab:green', ls='-.', lw=2, zorder=2,
           label=f'median = {median:.2f}')

ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=90, fontsize=7)
ax.set_xlabel("Wire #")
ax.set_ylabel("Volume [nm^3]")
ax.set_title(f"Per-wire volume — {SAMPLE_NBR}")
ax.grid(True, axis='y', alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()