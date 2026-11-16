import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import prince
import os

# Chargement des données
script_dir = os.path.dirname(os.path.abspath(__file__))
data = pd.read_excel(os.path.join(script_dir, '..', 'adult_clean.xlsx'))

print(f"ACM - Adult: {data.shape[0]} obs, {data.shape[1]} var")
print(f"Variables: {', '.join(data.columns)}")

# ACM
mca = prince.MCA(n_components=5, n_iter=3, random_state=42)
mca = mca.fit(data)

# Valeurs propres
eigenvalues = mca.eigenvalues_
total_inertia = sum(eigenvalues)
variance_pct = eigenvalues / total_inertia * 100
cumulative = np.cumsum(variance_pct)

print("\nValeurs propres:")
for i, (eig, var, cum) in enumerate(zip(eigenvalues, variance_pct, cumulative)):
    print(f"Dim.{i+1}: {eig:.4f} ({var:.1f}%, cumul: {cum:.1f}%)")

# Coordonnées
col_coords = mca.column_coordinates(data)
row_coords = mca.row_coordinates(data)
col_contrib = mca.column_contributions_ * 100

# GRAPHIQUE 1: Scree Plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(range(1, len(eigenvalues)+1), variance_pct, color='steelblue', alpha=0.7)
ax.plot(range(1, len(eigenvalues)+1), cumulative, 'ro-')
ax.axhline(y=80, color='green', linestyle='--', alpha=0.7)
ax.set_xlabel('Dimensions')
ax.set_ylabel('Variance (%)')
ax.set_title('Éboulis des Valeurs Propres - ACM')
plt.tight_layout()
plt.show()

# GRAPHIQUE 2: Carte des modalités
fig, ax = plt.subplots(figsize=(12, 10))
colors = plt.cm.tab10(np.linspace(0, 1, len(data.columns)))
color_dict = {var: colors[i] for i, var in enumerate(data.columns)}

for idx, row in col_coords.iterrows():
    var_name = idx.split('__')[0]
    modalite = idx.split('__')[1] if '__' in idx else idx
    ax.scatter(row.iloc[0], row.iloc[1], c=[color_dict.get(var_name, 'gray')], s=100)
    ax.annotate(modalite, (row.iloc[0], row.iloc[1]), fontsize=9)

for var, color in color_dict.items():
    ax.scatter([], [], c=[color], label=var)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_xlabel(f'Dim 1 ({variance_pct[0]:.1f}%)')
ax.set_ylabel(f'Dim 2 ({variance_pct[1]:.1f}%)')
ax.set_title('Carte des Modalités - ACM')
ax.legend(title='Variables', bbox_to_anchor=(1.02, 1))
plt.tight_layout()
plt.show()

# GRAPHIQUE 3: Carte des individus
fig, ax = plt.subplots(figsize=(10, 8))
ax.scatter(row_coords.iloc[:, 0], row_coords.iloc[:, 1], c='steelblue', s=80, alpha=0.7)
for i, (x, y) in enumerate(zip(row_coords.iloc[:, 0], row_coords.iloc[:, 1])):
    ax.annotate(str(i+1), (x, y), fontsize=8)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_xlabel(f'Dim 1 ({variance_pct[0]:.1f}%)')
ax.set_ylabel(f'Dim 2 ({variance_pct[1]:.1f}%)')
ax.set_title('Carte des Individus - ACM')
plt.tight_layout()
plt.show()

# GRAPHIQUE 4: Contributions
fig, axes = plt.subplots(1, 2, figsize=(14, 8))
for i, ax in enumerate(axes):
    contrib = pd.Series(col_contrib[:, i], index=col_coords.index).sort_values()
    ax.barh(range(len(contrib)), contrib.values, color=['steelblue', 'darkorange'][i])
    ax.set_yticks(range(len(contrib)))
    ax.set_yticklabels(contrib.index)
    ax.axvline(100/len(col_contrib), color='red', linestyle='--')
    ax.set_title(f'Contributions à Dim {i+1}')
plt.tight_layout()
plt.show()

print("\nAnalyse terminée.")
