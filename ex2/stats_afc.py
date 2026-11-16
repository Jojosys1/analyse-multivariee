import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import prince
import seaborn as sns
import os
from scipy.stats import chi2_contingency

# Chargement des données
script_dir = os.path.dirname(os.path.abspath(__file__))
contingency = pd.read_excel(os.path.join(script_dir, '..', 'housetasks.xlsx'), index_col=0)

print(f"AFC - Housetasks: {contingency.shape[0]} lignes, {contingency.shape[1]} colonnes")
print(contingency)

# Test du Chi-2
chi2, p_value, dof, _ = chi2_contingency(contingency)
print(f"\nChi-2 = {chi2:.2f}, p-value = {p_value:.2e}")

# AFC
ca = prince.CA(n_components=3, n_iter=10, random_state=42)
ca = ca.fit(contingency)

# Valeurs propres
eigenvalues = ca.eigenvalues_
total_inertia = ca.total_inertia_
variance_pct = [e / total_inertia * 100 for e in eigenvalues]
cumulative = np.cumsum(variance_pct)

print(f"\nInertie totale: {total_inertia:.4f}")
for i, (eig, var, cum) in enumerate(zip(eigenvalues, variance_pct, cumulative)):
    print(f"Dim.{i+1}: {eig:.4f} ({var:.1f}%, cumul: {cum:.1f}%)")

# Coordonnées
row_coords = ca.row_coordinates(contingency)
row_coords.columns = [f'Dim.{i+1}' for i in range(row_coords.shape[1])]
col_coords = ca.column_coordinates(contingency)
col_coords.columns = [f'Dim.{i+1}' for i in range(col_coords.shape[1])]

# Contributions
row_contrib = pd.DataFrame(ca.row_contributions_ * 100, index=contingency.index,
                           columns=[f'Dim.{i+1}' for i in range(len(eigenvalues))])

# GRAPHIQUE 1: Scree Plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(range(1, len(eigenvalues)+1), variance_pct, color='steelblue', alpha=0.7)
ax.plot(range(1, len(eigenvalues)+1), cumulative, 'ro-')
ax.set_xlabel('Dimensions')
ax.set_ylabel('Inertie (%)')
ax.set_title('Éboulis des Valeurs Propres - AFC')
plt.tight_layout()
plt.show()

# GRAPHIQUE 2: Carte factorielle
fig, ax = plt.subplots(figsize=(12, 10))
for idx, row in row_coords.iterrows():
    ax.scatter(row['Dim.1'], row['Dim.2'], c='blue', s=100, marker='o')
    ax.annotate(idx, (row['Dim.1'], row['Dim.2']), fontsize=10, color='blue', fontweight='bold')
for idx, row in col_coords.iterrows():
    ax.scatter(row['Dim.1'], row['Dim.2'], c='red', s=150, marker='^')
    ax.annotate(idx, (row['Dim.1'], row['Dim.2']), fontsize=11, color='red', fontweight='bold')
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_xlabel(f'Dim 1 ({variance_pct[0]:.1f}%)')
ax.set_ylabel(f'Dim 2 ({variance_pct[1]:.1f}%)')
ax.set_title('Carte Factorielle AFC')
ax.legend(['Tâches', 'Personnes'], loc='best')
plt.tight_layout()
plt.show()

# GRAPHIQUE 3: Contributions
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
for i, (ax, dim) in enumerate(zip(axes, ['Dim.1', 'Dim.2'])):
    contrib = row_contrib[dim].sort_values()
    ax.barh(range(len(contrib)), contrib.values, color=['steelblue', 'darkorange'][i])
    ax.set_yticks(range(len(contrib)))
    ax.set_yticklabels(contrib.index)
    ax.axvline(100/len(contingency), color='red', linestyle='--')
    ax.set_title(f'Contributions à {dim}')
plt.tight_layout()
plt.show()

# GRAPHIQUE 4: Heatmaps
row_profiles = contingency.div(contingency.sum(axis=1), axis=0) * 100
fig, axes = plt.subplots(1, 2, figsize=(14, 8))
sns.heatmap(contingency, annot=True, fmt='d', cmap='YlOrRd', ax=axes[0])
axes[0].set_title('Tableau de Contingence')
sns.heatmap(row_profiles, annot=True, fmt='.1f', cmap='Blues', ax=axes[1])
axes[1].set_title('Profils Lignes (%)')
plt.tight_layout()
plt.show()

print("\nAnalyse terminée.")
