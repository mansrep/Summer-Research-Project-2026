import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.mixture import GaussianMixture
from scipy.stats import norm

REMOVE_OUTLIERS = True

files = [
    ("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5022).csv", "#5033 @ #5022"),
    ("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5023).csv", "#5033 @ #5023"),
    ("MnAs_GaAs_summer_project_sample_overview1(#5033 @ #5024).csv", "#5033 @ #5024"),
    ("MnAs_GaAs_summer_project_sample_overview1(#5031 @ #5024).csv", "#5031 @ #5024"),
    ("MnAs_GaAs_summer_project_sample_overview1(#5034 @ #5024).csv", "#5034 @ #5024"),
]

categories = ['A','B','C','D','E','F','G']
frames = []
for path, name in files:
    d = pd.read_csv(path, sep=';')
    d.columns = [c.strip().replace('\ufeff', '') for c in d.columns]
    d["sample"] = name          # keep track of which file each wire came from
    frames.append(d)

df_all = pd.concat(frames, ignore_index=True)
sample_nbr = "all samples pooled"

df = df_all[categories].apply(pd.to_numeric, errors='coerce')

fig, axes = plt.subplots(2, 4, figsize=(15, 8))
cutoffs = {"A": (20, None), "D": (None, 1000), "F": (None, 1000), "G": (None, 1000)}

for ax, cat in zip(axes.ravel(), categories):
    vals = df[cat].dropna().values

    if REMOVE_OUTLIERS:
        lo, hi = cutoffs.get(cat, (None, None))
        if lo is not None: vals = vals[vals >= lo]
        if hi is not None: vals = vals[vals <= hi]
    X = vals.reshape(-1, 1)

    # try 1–3 components, keep the one with the lowest BIC
    candidates = range(1, 4)
    models = [GaussianMixture(n, covariance_type='full', random_state=42).fit(X)
              for n in candidates]
    bics = [m.bic(X) for m in models]
    best_k = candidates[int(np.argmin(bics))]
    gmm = models[int(np.argmin(bics))]

    ax.hist(vals, bins=np.histogram_bin_edges(vals, bins='fd'), density=True, alpha=0.4, color='gray', edgecolor='k')
    x_range = np.linspace(vals.min()-1, vals.max()+1, 1000)
    total = np.zeros_like(x_range)
    for k in range(gmm.n_components):
        mean = gmm.means_[k,0]; std = np.sqrt(gmm.covariances_[k,0,0]); w = gmm.weights_[k]
        comp = w * norm.pdf(x_range, mean, std)
        ax.plot(x_range, comp, linewidth=2)
        total += comp
    ax.plot(x_range, total, 'k--', linewidth=2)
    ax.scatter(gmm.means_[:,0], np.zeros(gmm.n_components), s=150, c='red', marker='X', zorder=5)

    ax.set_title(f"Category {cat} — best fit: {best_k} components")
    ax.set_xlabel("[nm]"); ax.set_ylabel("Density")
    ax.grid(True, alpha=0.3)
fig.suptitle(sample_nbr)
plt.tight_layout()
plt.show()