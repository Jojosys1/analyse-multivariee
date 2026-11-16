# Pistes d'amélioration — Analyse multivariée

## C'est quoi
Rapport « Base de données » en 4 exercices d'analyse multivariée :
ACP (`ex1`), AFC (`ex2`), ACM (`ex3`), AFDM (`ex4`).

## État actuel
- Un dossier par exercice (`ex1` … `ex4`) avec script, figures et rapport LaTeX.
- Données : `wine.xlsx`, `housetasks.xlsx`, `adult_clean.xlsx`, `bank.xlsx`.
- Scripts mélangés Python (`*_analysis.py`) et R (`RAPPORT_base_de_données1.Rmd`).

## Pistes (courtes)
- Choisir un seul langage par exercice (tout Python **ou** tout R), pas les deux.
- Compiler les 4 rapports LaTeX en un seul PDF `rapport_analyse_multivariee.pdf`.
- Ajouter un `README.md` : plan du rapport, méthode par exercice, figures clés.
- Nommer les figures sans espaces ni accents (`biplot acm.png` → `biplot_acm.png`).
- Mettre les données partagées dans un dossier `donnees/` unique.
- Résumer les résultats dans un tableau (valeurs propres, % inertie) dans le README.

## Mini-prompt
> Unifie les 4 exercices, compile-les en un PDF, range les données dans `donnees/`,
> et écris un README avec la méthode et les résultats de chaque exercice.
