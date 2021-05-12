import pandas as pd
from src import (
    utils,
    reprise_donnees,
    reprise_check
)
from fpdf import FPDF

if False:
    reprise_check.check_env(env="PRODUCTION")


if False:
    df_villes = pd.read_csv(utils.sources.get('cog_communes'))
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_colwidth', None)
    print(df_villes.head(1000))


if False:
    latin_str = 'Saint-Martin-le-Nœud'
    document = FPDF()
    document.add_font('DejaVu', '', '/home/crxadmin/.local/share/fonts/DejaVuSansCondensed.ttf', uni=True)
    document.set_font('DejaVu', '', 14)
    document.add_page()
    document.cell(w=0, txt="Welcome to the nice city of " + latin_str)
    document.output("hello_world.pdf")


if False:
    # df_villes = pd.read_csv('csv/output/frontend_localisation_villes.csv', encoding='utf-8')
    df_villes = pd.read_csv(utils.sources.get('cog_communes'))
    df_noeud = df_villes[df_villes['COM'] == '60586'].iloc[0]
    print(df_noeud)


if False:
    latin_str = 'Saint-Martin-le-Nœud'
    print(latin_str)

    utf = latin_str.encode('latin-1', 'replace').decode('latin-1')
    print(utf)

if False:
    # reprise_check.check_moa()
    reprise_check.check_prod()

if False:
    df_reprise = pd.read_csv('csv/output/reprise/frontend_localisation_villes.csv', low_memory=False)
    df_reprise = df_reprise[df_reprise['ville_newId'].isna()]
    # df_reprise = pd.read_csv(utils.output.get('reprise_ville'), low_memory=False)
    # group_nccenr = df_reprise.groupby('ville_NCCENR').size()
    group_nccenr = df_reprise.groupby('ville_NCCENR')['ville_NCCENR'].count().sort_values(ascending=True)
    print(group_nccenr)
    # reprise_donnees.run()


if False:
    df_departements = pd.read_csv('csv/sources/departement2021.csv')
    #df_departements.info()

    df_regions = pd.read_csv('csv/sources/region2021.csv')
    #df_regions.info()

    df_villes = pd.read_csv('csv/output/frontend_localisation_villes.csv')
    #df_villes.info()
    """
        'cp': 'csv/output/frontend_localisation_cp.csv',
        'departements': 'csv/output/frontend_localisation_departements.csv',
        'regions': 'csv/output/frontend_localisation_regions.csv',
    """

    df_regions = pd.read_csv('csv/output/frontend_localisation_regions.csv')
    #df_regions.info()

    df_dep = pd.read_csv('csv/output/frontend_localisation_departements.csv')
    #df_dep.info()

    df_cp = pd.read_csv('csv/output/frontend_localisation_cp.csv')
    #df_cp.info()

    df_reprise = pd.read_csv(utils.output.get('reprise_ville'))
    df_reprise.info()