import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import prince
import os

# Chargement des données
script_dir = os.path.dirname(os.path.abspath(__file__))
bank = pd.read_excel(os.path.join(script_dir, '..', 'bank.xlsx'))

# Types de variables
bank['age'] = bank['age'].astype(float)
bank['balance'] = bank['balance'].astype(float)
for col in ['job', 'marital', 'education', 'housing', 'loan']:
    bank[col] = bank[col].astype('category')

num_vars = bank.select_dtypes(include=[np.number]).columns.tolist()
cat_vars = bank.select_dtypes(include=['category']).columns.tolist()

print(f"AFDM - Bank: {bank.shape[0]} obs, {bank.shape[1]} var")
print(f"Quanti: {', '.join(num_vars)} | Quali: {', '.join(cat_vars)}")

# AFDM
famd = prince.FAMD(n_components=5, n_iter=3, random_state=42)
famd = famd.fit(bank)

# Valeurs propres
eigenvalues = famd.eigenvalues_
total_inertia = sum(eigenvalues)
variance_pct = eigenvalues / total_inertia * 100
cumulative = np.cumsum(variance_pct)

print("\nValeurs propres:")
for i, (eig, var, cum) in enumerate(zip(eigenvalues, variance_pct, cumulative)):
    print(f"Dim.{i+1}: {eig:.4f} ({var:.1f}%, cumul: {cum:.1f}%)")

# Coordonnées
quanti_coords = famd.column_coordinates_
quanti_coords.columns = [f'Dim.{i+1}' for i in range(quanti_coords.shape[1])]
row_coords = famd.row_coordinates(bank)
row_coords.columns = [f'Dim.{i+1}' for i in range(row_coords.shape[1])]

# GRAPHIQUE 1: Scree Plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(range(1, len(eigenvalues)+1), variance_pct, color='steelblue', alpha=0.7)
ax.plot(range(1, len(eigenvalues)+1), cumulative, 'ro-')
ax.axhline(y=80, color='green', linestyle='--', alpha=0.7)
ax.set_xlabel('Dimensions')
ax.set_ylabel('Variance (%)')
ax.set_title('Éboulis des Valeurs Propres - AFDM')
plt.tight_layout()
plt.show()

# GRAPHIQUE 2: Carte des individus (par statut marital)
fig, ax = plt.subplots(figsize=(10, 8))
colors_map = {'single': '#e41a1c', 'married': '#377eb8', 'divorced': '#4daf4a'}
colors = [colors_map.get(str(m), 'gray') for m in bank['marital']]
ax.scatter(row_coords['Dim.1'], row_coords['Dim.2'], c=colors, s=80, alpha=0.7, edgecolors='black')
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_xlabel(f'Dim 1 ({variance_pct[0]:.1f}%)')
ax.set_ylabel(f'Dim 2 ({variance_pct[1]:.1f}%)')
ax.set_title('Carte des Individus (par statut marital)')
for label, color in colors_map.items():
    ax.scatter([], [], c=color, label=label)
ax.legend(title='Marital')
plt.tight_layout()
plt.show()

# GRAPHIQUE 3: Cercle des corrélations
fig, ax = plt.subplots(figsize=(8, 8))
ax.add_patch(plt.Circle((0, 0), 1, fill=False, color='gray', linestyle='--'))
for var in num_vars:
    if var in quanti_coords.index:
        x, y = quanti_coords.loc[var, 'Dim.1'], quanti_coords.loc[var, 'Dim.2']
        ax.arrow(0, 0, x, y, head_width=0.05, head_length=0.03)
        ax.text(x*1.15, y*1.15, var, ha='center', fontsize=10, fontweight='bold')
ax.set_xlim(-1.3, 1.3)
ax.set_ylim(-1.3, 1.3)
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_xlabel(f'Dim 1 ({variance_pct[0]:.1f}%)')
ax.set_ylabel(f'Dim 2 ({variance_pct[1]:.1f}%)')
ax.set_title('Cercle des Corrélations')
ax.set_aspect('equal')
plt.tight_layout()
plt.show()

# GRAPHIQUE 4: Distribution des variables qualitatives
fig, axes = plt.subplots(2, 3, figsize=(12, 8))
axes = axes.flatten()
for i, col in enumerate(cat_vars):
    if i < len(axes):
        bank[col].value_counts().plot(kind='bar', ax=axes[i], color='steelblue')
        axes[i].set_title(col)
        axes[i].tick_params(axis='x', rotation=45)
for j in range(len(cat_vars), len(axes)):
    axes[j].axis('off')
plt.tight_layout()
plt.show()

# GRAPHIQUE 5: Carte des individus (par éducation)
fig, ax = plt.subplots(figsize=(10, 8))
edu_colors = {'primary': '#e41a1c', 'secondary': '#377eb8', 'tertiary': '#4daf4a', 'unknown': '#984ea3'}
colors = [edu_colors.get(str(e), 'gray') for e in bank['education']]
ax.scatter(row_coords['Dim.1'], row_coords['Dim.2'], c=colors, s=80, alpha=0.7, edgecolors='black')
ax.axhline(0, color='gray', linewidth=0.5)
ax.axvline(0, color='gray', linewidth=0.5)
ax.set_xlabel(f'Dim 1 ({variance_pct[0]:.1f}%)')
ax.set_ylabel(f'Dim 2 ({variance_pct[1]:.1f}%)')
ax.set_title('Carte des Individus (par éducation)')
for label, color in edu_colors.items():
    ax.scatter([], [], c=color, label=label)
ax.legend(title='Education')
plt.tight_layout()
plt.show()

print("\nAnalyse terminée.")
