"""
PCA analysis of MnAs/GaAs nanowire segment lengths.
Handles: semicolon CSV, stray text cells, missing values.
Produces: scree plot, loadings heatmap, PC1-PC2 score plot colored by a flag.
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# ======================= SETTINGS =======================
CSV_PATH   = "MnAs_GaAs_summer_project_sample_overview1(#5031 @ #5024).csv"
SAMPLE_NBR = "#5031 @ #5024"
SEGMENTS   = ['A', 'B', 'C', 'D', 'E', 'F']   # segments to include
COLOR_BY   = 'Bottom'                         # flag to color the score plot by
# ========================================================

# --- load & clean ---
df = pd.read_csv(CSV_PATH, sep=';')
#df = df[df["A"] >= 20]
df.columns = [c.strip().replace('\ufeff', '') for c in df.columns]
for s in SEGMENTS:
    df[s] = pd.to_numeric(df[s], errors='coerce')   # stray text -> NaN

# PCA needs complete rows; keep only wires with all segments measured
data = df.dropna(subset=SEGMENTS).copy()
X_raw = data[SEGMENTS].values
n_used = len(data)
print(f"Wires with all {len(SEGMENTS)} segments measured: {n_used} of {len(df)}")
if n_used < len(SEGMENTS) + 2:
    print("WARNING: very few complete rows; PCA may be unstable.")

# --- standardize (each segment to mean 0, sd 1) so no segment dominates by scale ---
X = StandardScaler().fit_transform(X_raw)

# --- fit PCA ---
pca = PCA()
scores = pca.fit_transform(X)
evr = pca.explained_variance_ratio_

print("\nExplained variance ratio per PC:")
for i, v in enumerate(evr):
    print(f"  PC{i+1}: {v*100:5.1f}%   (cumulative {np.cumsum(evr)[i]*100:5.1f}%)")

print("\nLoadings (segment contribution to each PC):")
header = "      " + "".join(f"{s:>7}" for s in SEGMENTS)
print(header)
for i in range(len(SEGMENTS)):
    print(f"PC{i+1}: " + "".join(f"{v:+7.2f}" for v in pca.components_[i]))

# ======================= PLOTS =======================
fig, axes = plt.subplots(1, 3, figsize=(18, 5.5))

# (1) scree plot
ax = axes[0]
pcs = np.arange(1, len(evr) + 1)
ax.bar(pcs, evr * 100, color='tab:blue', alpha=0.8, edgecolor='k')
ax.plot(pcs, np.cumsum(evr) * 100, 'o-', color='tab:red', label='cumulative')
ax.set_xlabel("Principal component"); ax.set_ylabel("Variance explained [%]")
ax.set_title("Scree plot"); ax.set_xticks(pcs)
ax.legend(); ax.grid(axis='y', alpha=0.3)

# (2) loadings heatmap
ax = axes[1]
L = pca.components_[:len(SEGMENTS)]
im = ax.imshow(L, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
ax.set_xticks(range(len(SEGMENTS))); ax.set_xticklabels(SEGMENTS)
ax.set_yticks(range(len(SEGMENTS))); ax.set_yticklabels([f"PC{i+1}" for i in range(len(SEGMENTS))])
for i in range(len(SEGMENTS)):
    for j in range(len(SEGMENTS)):
        ax.text(j, i, f"{L[i, j]:.2f}", ha='center', va='center', fontsize=8)
ax.set_title("Loadings (segment → PC)")
plt.colorbar(im, ax=ax, fraction=0.046)

# (3) PC1 vs PC2 score plot, colored by a flag
ax = axes[2]
if COLOR_BY in data.columns:
    flag = data[COLOR_BY].fillna('NA')
    palette = {'Yes': 'tab:red', 'No': 'tab:blue', '?': 'gray', 'NA': 'lightgray'}
    for val in flag.unique():
        m = (flag == val).values
        ax.scatter(scores[m, 0], scores[m, 1], s=60, alpha=0.8, edgecolor='k',
                   c=palette.get(val, 'green'), label=f"{COLOR_BY}={val}")
    ax.legend(fontsize=8)
else:
    ax.scatter(scores[:, 0], scores[:, 1], s=60, alpha=0.8, edgecolor='k', c='tab:blue')
ax.axhline(0, color='gray', lw=0.5); ax.axvline(0, color='gray', lw=0.5)
ax.set_xlabel(f"PC1 ({evr[0]*100:.0f}%)"); ax.set_ylabel(f"PC2 ({evr[1]*100:.0f}%)")
ax.set_title("Score plot (PC1 vs PC2)")
ax.grid(alpha=0.3)

fig.suptitle(f"PCA of segments — {SAMPLE_NBR}  (n={n_used})", fontsize=14)
plt.tight_layout()
#plt.savefig('/home/claude/pca_out.png', dpi=120, bbox_inches='tight')
plt.show()