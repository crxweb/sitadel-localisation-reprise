import pandas as pd
from src import (
    utils,
    reprise_donnees,
    reprise_check
)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

df_departements = pd.read_csv('csv/sources/departement2021.csv')
# df_departements.info()

df_regions = pd.read_csv('csv/sources/region2021.csv')
# df_regions.info()

df_villes = pd.read_csv('csv/output/frontend_localisation_villes.csv')
group_insee = df_villes.groupby('ville_COM')['ville_COM'].count().sort_values(ascending=True)
#df_villes.info()
#print(group_insee)
"""
    'cp': 'csv/output/frontend_localisation_cp.csv',
    'departements': 'csv/output/frontend_localisation_departements.csv',
    'regions': 'csv/output/frontend_localisation_regions.csv',
"""

df_regions = pd.read_csv('csv/output/frontend_localisation_regions.csv')
# df_regions.info()

df_dep = pd.read_csv('csv/output/frontend_localisation_departements.csv')
# df_dep.info()

if False:
    df_cp = pd.read_csv('csv/output/frontend_localisation_cp.csv', low_memory=False, dtype=object)
    df_cp.info()
    print(df_cp.describe())
    group_insee = df_cp.groupby('cp_Code_commune_INSEE')['cp_Code_commune_INSEE'].count().sort_values(ascending=True)
    print(group_insee)

df_reprise = pd.read_csv(utils.output.get('reprise_ville'))
# df_reprise.info()

