import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import fisher_exact

#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5022).csv", sep=';'), "#5033 @ #5022"
df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", sep=';'), "#5033 @ #5023"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';'), "#5033 @ #5024"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5031 @ #5024).csv", sep=';'), "#5031 @ #5024"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5034 @ #5024).csv", sep=';'), "#5034 @ #5024"

categories = ["Bottom", "Top", "Nanocluster?"]

pair = df[['Bottom', 'Nanocluster?']].apply(lambda s: s.map({'Yes': 1, 'No': 0})).dropna()

pair['Bottom'] = pd.Categorical(pair['Bottom'], categories=[0, 1])
pair['Nanocluster?'] = pd.Categorical(pair['Nanocluster?'], categories=[0, 1])

ct = pd.crosstab(pair['Bottom'], pair['Nanocluster?'], dropna=False)
odds, p = fisher_exact(ct)

ct.index = ct.index.map({0: 'No', 1: 'Yes'})
ct.columns = ct.columns.map({0: 'No', 1: 'Yes'})

plt.figure(figsize=(6,5))
ax = sns.heatmap(ct, annot=True, fmt='d', cmap='Blues',
                 cbar_kws={'label': 'Count'}, linewidths=1, linecolor='white',
                 square=True, annot_kws={'size': 16})
ax.set_xlabel('Nanocluster on NW?')
ax.set_ylabel('Transformed Bottom?')
ax.set_title(f"Bottom vs Nanocluster, n = {len(pair)}")
plt.suptitle(sample_nbr)
plt.tight_layout()
plt.show()
# (Fisher exact p = {p:.3f}.   i line 32 kan den läggas till