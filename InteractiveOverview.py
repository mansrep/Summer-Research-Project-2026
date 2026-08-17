import matplotlib.pyplot as plt
from matplotlib.widgets import RadioButtons
import numpy as np
import pandas as pd

# ----------------------------------------------------------------------
# load data
# ----------------------------------------------------------------------
df = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5022).csv", sep=';')
df = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", sep=';') 
df = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';') 
df = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5031 @ #5024).csv", sep=';')
df = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5034 @ #5024).csv", sep=';')

num_categories = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
binary_flags   = ['Nanocluster?', 'Top', 'Bottom', 'Au particle?']
rng = np.random.default_rng(42)

df = df.dropna(subset=num_categories, how='all')
for cat in num_categories:
    df[cat] = pd.to_numeric(df[cat], errors='coerce')

rng = np.random.default_rng(42)
#df = df[df["Bottom"] == "Yes"]
# color for each possible binary value
value_colors = {'Yes': 'tab:red', 'No': 'tab:blue', '?': 'gray', 'NA': 'lightgray'}

# ----------------------------------------------------------------------
# figure layout: main plot on the right, radio buttons on the left
# ----------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(left=0.28)   # make room for the control panel

ax_radio = plt.axes([0.03, 0.4, 0.18, 0.25])   # [left, bottom, width, height]
radio = RadioButtons(ax_radio, ['None'] + binary_flags)
ax_radio.set_title("Color by:", fontsize=10)

def draw(color_by):
    ax.clear()
    seen = set()
    for xpos, cat in enumerate(num_categories):
        shifter = 0
        if color_by == 'None':
            vals = df[cat].dropna().values
            ax.scatter(np.full(len(vals), xpos), vals,
                       s=70, alpha=0.8, edgecolor='k', c='tab:blue', zorder=3)
        else:
            sub = df[[cat, color_by]].dropna(subset=[cat])
            flagvals = sub[color_by].fillna('NA')      # show missing flags too
            
            for val in flagvals.unique():
                rows = sub[flagvals == val]
                color = value_colors.get(val, 'green')
                label = f"{color_by} = {val}"
                jitter = rng.uniform(-0.08, 0.08, size=len(rows))
                ax.scatter(xpos + jitter, rows[cat].values,
                           s=70, alpha=0.8, edgecolor='k', c=color, zorder=3,
                           label=label if label not in seen else None)
                seen.add(label)
                sub_value = rows[cat].values
                sub_mean = sub_value.mean()
                sub_SD = sub_value.std(ddof=1)
                shifter += 0.03
                bar_xpos = xpos + 0.15 + shifter
                ax.errorbar(bar_xpos, sub_mean, yerr=sub_SD, fmt='o',
                            c=color,capsize=5, markersize=8, zorder=4)
                ax.annotate(f"{sub_mean:.1f}", (bar_xpos, sub_mean),
                            textcoords="offset points", xytext=(8, 0),
                            va='center', fontsize=8, color=color)
                

        # mean +/- SD across all points in the category
        vals = df[cat].dropna().values
        mean = vals.mean()
        SD = vals.std(ddof=1)
        ax.errorbar(xpos + 0.15, mean, yerr=SD, fmt='o',
                    color='black', capsize=5, markersize=8, zorder=4)
        ax.annotate(f"{mean:.1f}", (xpos + 0.15, mean),
                    textcoords="offset points", xytext=(8, 0),
                    va='center', fontsize=8, color='black')

    ax.set_xticks(range(len(num_categories)))
    ax.set_xticklabels(num_categories)
    ax.set_xlabel("Dimension")
    ax.set_ylabel("[nm]")
    title = "measurements by category"
    if color_by != 'None':
        title += f"  —  colored by {color_by}"
    ax.set_title(title)
    ax.grid(True, axis='y', alpha=0.3)
    if color_by != 'None':
        ax.legend(fontsize=8)
    fig.canvas.draw_idle()


radio.on_clicked(draw)
draw('None')      # initial render
plt.show()