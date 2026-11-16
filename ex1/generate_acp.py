import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import os

# Chargement des données
script_dir = os.path.dirname(os.path.abspath(__file__))
wine = pd.read_excel(os.path.join(script_dir, '..', 'wine.xlsx'))
wine_data = wine.iloc[:, :-1]

print(f"ACP - Wine: {wine_data.shape[0]} obs, {wine_data.shape[1]} var")

# Standardisation et ACP
wine_scaled = StandardScaler().fit_transform(wine_data)
pca = PCA()
scores = pca.fit_transform(wine_scaled)

# Valeurs propres
eig = pd.DataFrame({
    'Dim': [f'Dim.{i+1}' for i in range(len(pca.explained_variance_))],
    'Valeur propre': pca.explained_variance_,
    'Variance (%)': pca.explained_variance_ratio_ * 100,
    'Cumul (%)': np.cumsum(pca.explained_variance_ratio_) * 100
})
print("\nValeurs propres:")
print(eig.to_string(index=False))

# Corrélations variables-composantes
correlations = pca.components_.T * np.sqrt(pca.explained_variance_)

# GRAPHIQUE 1: Scree Plot
fig, ax = plt.subplots(figsize=(10, 6))
x = range(1, len(pca.explained_variance_ratio_) + 1)
ax.bar(x, pca.explained_variance_ratio_ * 100, color='steelblue', alpha=0.7, label='Variance')
ax.plot(x, np.cumsum(pca.explained_variance_ratio_) * 100, 'ro-', label='Cumulée')
ax.axhline(y=80, color='green', linestyle='--', alpha=0.7)
ax.set_xlabel('Composantes')
ax.set_ylabel('Variance (%)')
ax.set_title('Éboulis des Valeurs Propres')
ax.legend()
plt.tight_layout()
plt.show()

# GRAPHIQUE 2: Cercle des corrélations
fig, ax = plt.subplots(figsize=(10, 10))
ax.add_patch(plt.Circle((0, 0), 1, fill=False, color='gray', linestyle='--'))
for i, var in enumerate(wine_data.columns):
    ax.arrow(0, 0, correlations[i, 0], correlations[i, 1], head_width=0.05, head_length=0.03)
    ax.text(correlations[i, 0]*1.15, correlations[i, 1]*1.15, var, ha='center', fontsize=9)
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_xlabel(f'Dim 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
ax.set_ylabel(f'Dim 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
ax.set_title('Cercle des Corrélations')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()

# GRAPHIQUE 3: Projection des individus
fig, ax = plt.subplots(figsize=(12, 10))
colors = ['#e41a1c', '#377eb8', '#4daf4a']
for target, color, name in zip([0, 1, 2], colors, ['Classe 0', 'Classe 1', 'Classe 2']):
    mask = wine['target'] == target
    ax.scatter(scores[mask, 0], scores[mask, 1], c=color, label=name, alpha=0.7, s=80, edgecolors='black')
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_xlabel(f'Dim 1 ({pca.explained_variance_ratio_[0]*100:.1f}%)')
ax.set_ylabel(f'Dim 2 ({pca.explained_variance_ratio_[1]*100:.1f}%)')
ax.set_title('Projection des Individus')
ax.legend()
plt.tight_layout()
plt.show()

# GRAPHIQUE 4: Matrice de corrélation
fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(wine_data.corr(), dtype=bool))
sns.heatmap(wine_data.corr(), mask=mask, annot=True, fmt='.2f', cmap='RdBu_r', center=0, ax=ax)
ax.set_title('Matrice de Corrélation')
plt.tight_layout()
plt.show()

# GRAPHIQUE 5: Contributions
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].barh(wine_data.columns, (pca.components_[0]**2)*100, color='steelblue')
axes[0].axvline(100/len(wine_data.columns), color='red', linestyle='--')
axes[0].set_title('Contributions à Dim 1')
axes[1].barh(wine_data.columns, (pca.components_[1]**2)*100, color='darkorange')
axes[1].axvline(100/len(wine_data.columns), color='red', linestyle='--')
axes[1].set_title('Contributions à Dim 2')
plt.tight_layout()
plt.show()

print("\nAnalyse terminée.")
