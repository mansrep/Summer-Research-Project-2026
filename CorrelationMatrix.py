import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

WITH_NO_NON_TRANSFORMED_BOTTOMS = False
WITH_NO_TRANSFORMED_BOTTOMS = False
WITH_NO_F_OUTLIER = False

df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5022).csv", sep=';'), "#5033 @ #5022"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", sep=';'), "#5033 @ #5023"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", sep=';'), "#5033 @ #5024"
df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5031 @ #5024).csv", sep=';'), "#5031 @ #5024"
#df, sample_nbr = pd.read_csv("MnAs_GaAs_summer_project_sample_overview1(#5034 @ #5024).csv", sep=';'), "#5034 @ #5024"

categories = ["A", "B", "C", "D", "E", "F", "G"]
df = df[categories].apply(pd.to_numeric, errors='coerce')
if WITH_NO_TRANSFORMED_BOTTOMS:
    df = df[df["A"] <= 20]
if WITH_NO_NON_TRANSFORMED_BOTTOMS:
    df = df[df["A"] >= 20]
if WITH_NO_F_OUTLIER:
    df = df[df["F"] <= 150]
#df = df[df["C"] >= 225]

matrix = df.corr()
mask = np.triu(np.ones_like(matrix, dtype=bool), k=1)
plt.figure(figsize=(8,6))
sns.heatmap(matrix,mask=mask, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5)
plt.suptitle(sample_nbr)
plt.title("Correlation Heatmap")
plt.show()