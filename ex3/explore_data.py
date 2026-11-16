import pandas as pd
import numpy as np

# Charger les données
ac = pd.read_excel('../adult_clean.xlsx')
print("=== DONNEES ADULT_CLEAN ===")
print(ac)
print('\nShape:', ac.shape)
print('\nDtypes:')
print(ac.dtypes)

print('\n=== VALUE COUNTS PAR VARIABLE ===')
for col in ac.columns:
    print(f'\n{col}:')
    print(ac[col].value_counts())
