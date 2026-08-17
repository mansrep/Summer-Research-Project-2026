import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5022).csv", sep=';'), "#5033 @ #5022"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", sep=';'), "#5033 @ #5023"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';'), "#5033 @ #5024"
df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5031 @ #5024).csv", sep=';'), "#5031 @ #5024"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5034 @ #5024).csv", sep=';'), "#5034 @ #5024"

categories = ["Bottom", "Top", "Nanocluster?", "Au particle?"]

df = df[categories]

fig, axes = plt.subplots(1, 4, figsize=(15, 8))

for ax, cat in zip(axes.ravel(), categories):
    counts = df[cat].value_counts()
    ax.pie(counts, labels=counts.index, autopct='%1.1f%%', startangle=90)
    if cat == "Nanocluster?":
        ax.set_title("Nanocluster on NW?")
    elif cat == "Au particle?":
        ax.set_title("Au particle on NW?")
    else:
        ax.set_title(f"Transformed {cat}")

fig.suptitle(sample_nbr)
plt.tight_layout()
plt.show()