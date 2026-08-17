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
df['V_top'] = np.pi * (df['D'] / 2)**2 * df['E']
df['ratio']    = df['V_bottom'] / df['V_top']

# wire id
wire_col = next((c for c in df.columns if 'wire' in c.lower()), None)
labels = df[wire_col].astype(str).values if wire_col else np.arange(len(df)).astype(str)

ratios = df['ratio'].values
mean_r = ratios.mean()
median_r = np.median(ratios)

print(f"n wires: {len(df)}")
print(f"mean ratio (bottom/top):   {mean_r:.3f}")
print(f"median ratio (bottom/top): {median_r:.3f}")

# ==================== PLOT ====================
x = np.arange(len(df))
fig, ax = plt.subplots(figsize=(12, 6))

ax.scatter(x, ratios, s=70, color='tab:blue', edgecolor='k', zorder=3, label='wire ratio')

ax.axhline(mean_r,   color='tab:red',   ls='--', lw=2, zorder=2,
           label=f'mean = {mean_r:.2f}')
ax.axhline(median_r, color='tab:green', ls='-.', lw=2, zorder=2,
           label=f'median = {median_r:.2f}')
# reference line at ratio = 1 (equal top/bottom)
ax.axhline(1.0, color='gray', ls=':', lw=1, zorder=1, label='ratio = 1')

ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=90, fontsize=7)
ax.set_xlabel("Wire #")
ax.set_ylabel("Volume ratio  (bottom / top)")
ax.set_title(f"Per-wire volume ratio — {SAMPLE_NBR}")
ax.grid(True, axis='y', alpha=0.3)
ax.legend()
plt.tight_layout()
plt.show()