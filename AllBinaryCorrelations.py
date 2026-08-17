"""
Six 2x2 contingency tables, one per pair of the four binary flags.
Each cell = count of wires with that Yes/No combination.
Title shows phi coefficient and Fisher exact p-value.
Only genuine Yes/No used (?, blanks dropped per pair).
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from itertools import combinations
from scipy.stats import fisher_exact

CSV_PATH   = "MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv"
SAMPLE_NBR = "#5033 @ #5024"
flags = ['Bottom', 'Top', 'Nanocluster?', 'Au particle?']

df = pd.read_csv(CSV_PATH, sep=';')
df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]

pairs = list(combinations(flags, 2))          # 6 pairs
fig, axes = plt.subplots(2, 3, figsize=(15, 9))

for ax, (f1, f2) in zip(axes.ravel(), pairs):
    # keep only wires answered Yes/No on BOTH flags
    sub = df[[f1, f2]].apply(lambda s: s.map({'Yes': 1, 'No': 0})).dropna()

    # force full 2x2 even if a combo is empty
    sub[f1] = pd.Categorical(sub[f1], categories=[0, 1])
    sub[f2] = pd.Categorical(sub[f2], categories=[0, 1])
    ct = pd.crosstab(sub[f1], sub[f2], dropna=False)

    # phi and Fisher (guard against a constant flag / empty margin)
    try:
        phi = sub[f1].astype(float).corr(sub[f2].astype(float))
    except Exception:
        phi = np.nan
    try:
        _, p = fisher_exact(ct.values)
        p_txt = f"p={p:.3f}"
    except Exception:
        p_txt = "p=n/a"
    phi_txt = f"phi={phi:+.2f}" if not np.isnan(phi) else "phi=n/a"

    im = ax.imshow(ct.values, cmap='Blues', vmin=0)
    ax.set_xticks([0, 1]); ax.set_xticklabels(['No', 'Yes'])
    ax.set_yticks([0, 1]); ax.set_yticklabels(['No', 'Yes'])
    ax.set_xlabel(f2); ax.set_ylabel(f1)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, int(ct.values[i, j]), ha='center', va='center',
                    fontsize=16, color='black')
    ax.set_title(f"{f1} vs {f2}\n{phi_txt}, {p_txt}, n={len(sub)}", fontsize=10)

fig.suptitle(f"Binary flag pairwise contingency tables — {SAMPLE_NBR}", fontsize=14)
plt.tight_layout()
plt.show()