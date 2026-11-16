# Analyse multivariée — base de données

Rapport « Base de données » : quatre méthodes d'analyse multivariée appliquées
à quatre jeux de données, chacune avec son script, ses figures et un rapport LaTeX.

## Exercices

| Dossier | Méthode | Données | Script | Rapport |
|---|---|---|---|---|
| `ex1/` | ACP (Analyse en Composantes Principales) | `wine.xlsx` | `generate_acp.py` | `rapport_exercice1_ACP.tex` |
| `ex2/` | AFC (Analyse Factorielle des Correspondances) | `housetasks.xlsx` | `stats_afc.py` | `rapport_exercice2_AFC.tex` |
| `ex3/` | ACM (Analyse des Correspondances Multiples) | `adult_clean.xlsx` | `acm_analysis.py` | `rapport_exercice3_ACM.tex` |
| `ex4/` | AFDM (Analyse Factorielle de Données Mixtes) | `bank.xlsx` | `famd_analysis.py` | `rapport_exercice4_AFDM.tex` |

Les données sont à la racine du projet ; chaque script les charge via `../<fichier>.xlsx`.

## Autres fichiers

- `RAPPORT_base_de_données1.Rmd` : version R (R Markdown) du rapport, couvrant les 4 méthodes.
- `RAPPORT_base_de_données1.docx` : export Word du rapport R.
- `Travaux de maison_GMM2.pdf` : énoncé / rapport complémentaire.

## Prérequis

- **Python 3.10+** avec : `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `prince`.
- **R** (optionnel, pour le `.Rmd`) avec : `FactoMineR`, `readxl`, `GGally`.
- **LaTeX** pour compiler les rapports.

```bash
pip install pandas numpy matplotlib seaborn scikit-learn prince
```

## Utilisation

```bash
# Lancer un exercice (depuis son dossier)
cd ex1 && python generate_acp.py
cd ex2 && python stats_afc.py
cd ex3 && python acm_analysis.py
cd ex4 && python famd_analysis.py

# Compiler un rapport
cd ex1 && pdflatex rapport_exercice1_ACP.tex
```

## Résultats

Chaque dossier `ex*` contient les figures produites (éboulis des valeurs propres,
cercles de corrélation, cartes des individus/modalités, contributions).
