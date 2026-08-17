import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

data, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(LengthToNC#5033@#5023).csv", sep=';'), "#5033 @ #5023/24"

categories = ["Wire", "Total längd", "Längd till NC", "Längd av NC"]
data = data[categories]

fig, ax = plt.subplots(figsize=(9, 6))

for index, row in data.iterrows():
    Tot  = row["Total längd"]
    ToNC = row["Längd till NC"]
    OfNC = row["Längd av NC"]
    wire = row["Wire"]

    proc_bottom_NC = ToNC / Tot * 100
    proc_top_NC    = (ToNC + OfNC) / Tot * 100
    proc_middle_NC = (ToNC + OfNC / 2) / Tot * 100

    lower = proc_middle_NC - proc_bottom_NC
    upper = proc_top_NC - proc_middle_NC
    yerr = np.array([[lower], [upper]])     

    ax.errorbar(index, proc_middle_NC, yerr=yerr, fmt='o',
                color='tab:blue', capsize=6, markersize=7, zorder=3)

ax.set_xticks(range(len(data)))
ax.set_xticklabels(data["Wire"])
ax.set_xlabel("Wire")
ax.set_ylabel("Position along wire [%]")
ax.set_title(f"Nanocluster position per wire   {sample_nbr}")
ax.grid(True, axis='y', alpha=0.3)
ax.set_ylim(0,100)
ax.set_yticks(range(0, 101, 10))
plt.tight_layout()
plt.show()