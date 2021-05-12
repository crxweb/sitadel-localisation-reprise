import pandas as pd
from src import (
    utils,
    new_table_csv,
    reprise_check,
    reprise_donnees,
)
from colorama import Fore, Style
import sys
from fpdf import FPDF
from datetime import datetime

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def make_ville():
    print('', end="\n")
    print(Fore.BLUE + "--- PRODUCT table frontend_localisation_villes ---")
    new_table_csv.make_csv_ville()
    df_ville = pd.read_csv(utils.output.get('villes'), low_memory=False, dtype=object)
    df_ville.to_csv('mysql/data/frontend_localisation_villes.csv', index=None, header=False)
    print(Style.RESET_ALL + "\033[4mProcédure MYSQL : Table frontend_localisation_villes:\033[0m")
    print(df_ville.shape)
    s1 = [
        "Renommer l'actuelle table frontend_localisation_villes en frontend_localisation_villes_backup_001",
        'Importer la structure de la table : mysql/structure/frontend_localisation_villes.sql',
        'Importer les données csv : mysql/data/frontend_localisation_villes.csv',
        'Effectuer la reprise de données vides à NULL: mysql/requests/update_frontend_localisation_villes_01.sql'
    ]
    for i in s1:
        print(s1.index(i) + 1, end=' ')
        print(" ", i)
    print('', end="\n")
    """
    Procédure MYSQL : Table frontend_localisation_villes
    1 - Importer la structure de la table : mysql/structure/frontend_localisation_villes.sql
    2 - Importer les données csv : mysql/data/frontend_localisation_villes.csv
    3 - Effectuer la reprise de données vides à NULL: mysql/requests/update_frontend_localisation_villes_01.sql
    """


def make_codepostaux():
    print(Fore.BLUE + '--- PRODUCT table frontend_localisation_cp ---')
    new_table_csv.make_csv_cp()
    df_cp = pd.read_csv(utils.output.get('cp'), low_memory=False, dtype=object)
    df_cp.to_csv('mysql/data/frontend_localisation_cp.csv', index=None, header=False)

    print(Style.RESET_ALL + "\033[4mProcédure MYSQL : Table frontend_localisation_cp:\033[0m")
    print(df_cp.shape)
    s1 = [
        'Importer la structure de la table : mysql/structure/frontend_localisation_cp.sql',
        'Importer les données csv : mysql/data/frontend_localisation_cp.csv',
        'Effectuer la reprise de données vides à NULL: mysql/requests/update_frontend_localisation_cp_01.sql'
    ]
    for i in s1:
        print(s1.index(i) + 1, end=' ')
        print(" ", i)
    print('', end="\n")
    """
    Procédure MYSQL : Table frontend_localisation_cp
    1 - Importer la structure de la table : mysql/structure/frontend_localisation_cp.sql
    2 - Importer les données csv : mysql/data/frontend_localisation_cp.csv
    3 - Effectuer la reprise de données vides à NULL: mysql/requests/update_frontend_localisation_cp_01.sql
    """


def make_departement():
    print(Fore.BLUE + '--- PRODUCT table frontend_localisation_departements ---')
    new_table_csv.make_csv_departement()
    df_dep = pd.read_csv(utils.output.get('departements'), low_memory=False, dtype=object)
    df_dep.to_csv('mysql/data/frontend_localisation_departements.csv', index=None, header=False)

    print(Style.RESET_ALL + "\033[4mProcédure MYSQL : Table frontend_localisation_departements:\033[0m")
    print(df_dep.shape)
    s1 = [
        'Importer la structure de la table : mysql/structure/frontend_localisation_departements.sql',
        'Importer les données csv : mysql/data/frontend_localisation_departements.csv'
    ]
    for i in s1:
        print(s1.index(i) + 1, end=' ')
        print(" ", i)
    print('', end="\n")
    """
    Procédure MYSQL : Table frontend_localisation_departements
    1 - Importer la structure de la table : mysql/structure/frontend_localisation_departements.sql
    2 - Importer les données csv : mysql/data/frontend_localisation_departements.csv
    """


def make_region():
    print(Fore.BLUE + '--- PRODUCT table frontend_localisation_regions ---')
    new_table_csv.make_csv_region()
    df_reg = pd.read_csv(utils.output.get('regions'), low_memory=False, dtype=object)
    df_reg.to_csv('mysql/data/frontend_localisation_regions.csv', index=None, header=False)
    print(Style.RESET_ALL + "\033[4mProcédure MYSQL : Table frontend_localisation_regions:\033[0m")
    print(df_reg.shape)
    s1 = [
        'Importer la structure de la table : mysql/structure/frontend_localisation_regions.sql',
        'Importer les données csv : mysql/data/frontend_localisation_regions.csv'
    ]
    for i in s1:
        print(s1.index(i) + 1, end=' ')
        print(" ", i)
    print('', end="\n")
    """
    Procédure MYSQL : Table frontend_localisation_regions
    1 - Importer la structure de la table : mysql/structure/frontend_localisation_regions.sql
    2 - Importer les données csv : mysql/data/frontend_localisation_regions.csv
    """


def refonte(out_to_pdf=False, run_reprise=True):
    utils.say_something(message="Script is running, this may take severals minutes")
    if out_to_pdf:
        sys.stdout = open(utils.report.get('process_txt_method_mysql'), 'w')
    make_ville()
    make_codepostaux()
    make_departement()
    make_region()
    if run_reprise:
        reprise_donnees.run(enable_print=False, file_txt=utils.report.get('process_txt_method_mysql'))
    reprise_check.check_moa(enable_print=False, file_txt=utils.report.get('process_txt_method_mysql'))
    reprise_check.check_global(out_to_pdf=out_to_pdf)

    # Générer table permutation
    print(Fore.BLUE + "--- PRODUCT table frontend_localisation_villes_reprise ---")
    df_reprise = pd.read_csv(utils.output.get('reprise_ville'), low_memory=False)
    df_reprise.to_csv('mysql/data/frontend_localisation_villes_reprise.csv', index=None, header=False)
    print(Style.RESET_ALL + "\033[4mProcédure MYSQL : Table frontend_localisation_villes_reprise:\033[0m")
    print(df_reprise.shape,
          "Ajout colonne ville_newId faisant le lien avec la nouvelle table frontend_localisation_villes")
    s1 = [
        'Importer la structure de la table : mysql/structure/frontend_localisation_villes_reprise.sql',
        'Importer les données csv : mysql/data/frontend_localisation_villes_reprise.csv',
        'Effectuer reprise de données ville_newId 0 à NULL: mysql/requests/update_frontend_localisation_reprise_01.sql',
    ]
    for i in s1:
        print(s1.index(i) + 1, end=' ')
        print(" ", i)
    print('', end="\n")

    # Effectuer la reprise de données
    print(Fore.BLUE + "--- REPRISE DE DONNÉES ---")
    print(Style.RESET_ALL + "\033[4mProcédure MYSQL reprise données: Table frontend_localisation_villes:\033[0m")
    s1 = [
        "Copier la table frontend_localisation en frontend_localisation_backup_001",
        'Effectuer reprise de la table frontend_localisation: mysql/requests/update_frontend_localisation_v01.sql'
    ]
    for i in s1:
        print(s1.index(i) + 1, end=' ')
        print(" ", i)
    print('', end="\n")

    if out_to_pdf:
        sys.stdout.close()
        current_date = datetime.today().strftime('%d/%m/%Y %H:%M')
        pdf = FPDF(orientation='portrait')
        pdf.add_page()
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt="Sitadel le " + current_date,
                 ln=1, align='C')
        pdf.cell(200, 10, txt="Reprise des données de localisation",
                 ln=1, align='C')
        pdf.cell(190, 10, txt="Méthodologie: Créations des nouvelles tables et reprise de données",
                 ln=1, align='C', border=1)
        pdf.set_font("Arial", size=8)
        f = open(utils.report.get('process_txt_method_mysql'), "r")
        for x in f:
            x = x.replace('[34m', '')
            x = x.replace('[0m[4m', '')
            x = x.replace('[95m', '')
            x = x.replace('[0m', '')
            pdf.cell(200, 5, txt=x, ln=1)
        pdf.output(utils.report.get('process_pdf_method_mysql'))


# refonte(out_to_pdf=True, run_reprise=False)
utils.generate_documentation()





