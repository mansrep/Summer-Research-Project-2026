import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


data, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5022).csv", sep=';'), "#5033 @ #5022"
#data, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", sep=';'), "#5033 @ #5023"
data, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';'), "#5033 @ #5024"
#data, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5031 @ #5024).csv", sep=';'), "#5031 @ #5024"
#data, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5034 @ #5024).csv", sep=';'), "#5034 @ #5024"

data = data.dropna(subset=["A", "C", "G"])
if sample_nbr == "#5033 @ #5024":
    data = data[data["wire #"] != 21]
fig, ax = plt.subplots(figsize=(9, 6))
all_to_bottom_segment_TB = []
all_to_bottom_segment_nTB = []
all_to_middle_of_bottom_segment_TB = []
all_to_middle_of_bottom_segment_nTB = []
seen = []
for i, (index, row) in enumerate(data.iterrows()):
    Tot  = row["G"] + row["A"] + row["C"]
    ToSeg = row["G"]
    OfSeg = row["A"]
    wire = row["wire #"]
    bottom = row["Bottom"]
    colour = "grey"
    

    proc_bottom_Seg = ToSeg / Tot * 100
    proc_top_Seg    = (ToSeg + OfSeg) / Tot * 100
    proc_middle_Seg = (ToSeg + OfSeg / 2) / Tot * 100

    lower = proc_middle_Seg - proc_bottom_Seg
    upper = proc_top_Seg - proc_middle_Seg
    yerr = np.array([[lower], [upper]])    
    if bottom == "Yes":
        colour = "tab:blue"
        all_to_bottom_segment_TB.append(proc_bottom_Seg)
        all_to_middle_of_bottom_segment_TB.append(proc_middle_Seg)
    elif bottom == "No":
        colour = "tomato"
        all_to_bottom_segment_nTB.append(proc_bottom_Seg)
        all_to_middle_of_bottom_segment_nTB.append(proc_middle_Seg)
    label = f"{colour} = Transformed?: {bottom}"
    ax.errorbar(i, proc_middle_Seg, yerr=yerr, fmt='o',
                color=colour, capsize=6, markersize=7, zorder=3, label = label if label not in seen else None)
    seen.append(label)
        
mean_bottom_TB = np.mean(all_to_bottom_segment_TB)
mean_middle_TB = np.mean(all_to_middle_of_bottom_segment_TB)
mean_bottom_nTB = np.mean(all_to_bottom_segment_nTB)
mean_middle_nTB = np.mean(all_to_middle_of_bottom_segment_nTB)

ax.axhline(mean_bottom_nTB,   color='lightcoral',   ls='--', lw=2, zorder=2,
           label=f'mean to bottom of nTB seg = {mean_bottom_nTB:.2f}%')
ax.axhline(mean_middle_nTB,   color='firebrick',   ls='--', lw=2, zorder=2,
           label=f'mean to middle of nTB segment = {mean_middle_nTB:.2f}%')
ax.axhline(mean_bottom_TB,   color='cornflowerblue',   ls='--', lw=2, zorder=2,
           label=f'mean to bottom of TB seg = {mean_bottom_TB:.2f}%')
ax.axhline(mean_middle_TB,   color='royalblue',   ls='--', lw=2, zorder=2,
           label=f'mean to middle of TB segment = {mean_middle_TB:.2f}%')

ax.set_xticks(range(len(data)))
ax.set_xticklabels(data["wire #"])
ax.set_xlabel("wire #")
ax.set_ylabel("Position along wire [%]")
ax.set_title(f"Transformed segment position per wire   {sample_nbr}")
ax.grid(True, axis='y', alpha=0.3)
ax.set_ylim(0,100)
ax.set_yticks(range(0, 101, 10))
ax.legend()
plt.tight_layout()
plt.show()