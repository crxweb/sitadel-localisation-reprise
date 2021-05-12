import pyttsx3
import requests
import sys
import os
import glob
from pathlib import Path
import pandas as pd
from datetime import datetime
from fpdf import FPDF
from PyPDF2 import PdfFileMerger

sources = {
    'cog_communes': 'csv/sources/commune2021.csv',
    'cog_departements': 'csv/sources/departement2021.csv',
    'cog_regions': 'csv/sources/region2021.csv',
    'laposte_base_officielle': 'csv/sources/laposte_hexasmal.csv',
    'sitadel_villes': 'csv/sitadel/frontend_localisation_villes.csv',
    'communes_nouvelles': 'csv/insee_communes_nouvelles/',
    'sitback_moa_localisation': 'mysql/sitadel_backup_dbb/moa/frontend_localisation.csv',
    'sitback_moa_localisation_ville': 'mysql/sitadel_backup_dbb/moa/frontend_localisation_villes.csv',
    'sitback_prod_localisation': 'mysql/sitadel_backup_dbb/production/frontend_localisation.csv',
    'sitback_prod_localisation_ville': 'mysql/sitadel_backup_dbb/production/frontend_localisation_villes.csv',
}

output = {
    'villes': 'csv/output/frontend_localisation_villes.csv',
    'cp': 'csv/output/frontend_localisation_cp.csv',
    'departements': 'csv/output/frontend_localisation_departements.csv',
    'regions': 'csv/output/frontend_localisation_regions.csv',
    'communes_nouvelles': 'csv/output/insee_commmunes_nouvelles.csv',
    'communes_historique': 'csv/output/insee_communes_historique.csv',
    'reprise_ville_sub1': 'csv/output/reprise/ville_subset1.csv',
    'reprise_ville_sub2': 'csv/output/reprise/ville_subset2.csv',
    'reprise_ville': 'csv/output/reprise/frontend_localisation_villes.csv',
    'check_reprise_global': 'csv/output/reprise/check_global.csv',
    'check_reprise_moa': 'csv/output/reprise/check_moa.csv',
    'check_reprise_production': 'csv/output/reprise/check_production.csv',
}

report = {
    'process_txt_method_mysql': 'report/methodologie_mysql.txt',
    'process_pdf_method_mysql': 'report/methodologie_mysql.pdf',
    'process_pdf_method_collecte': 'report/methodologie_collecte.pdf',
    'process_pdf_method_creationtable': 'report/methodologie_creationtable.pdf',
    'check_reprise_moa_txt': 'report/reprise/check_moa.txt',
    'check_reprise_production_txt': 'report/reprise/check_production.txt',
}

# goto url and update your cookie
cookie = 'JSESSIONID=8017B037DC13189949F2443970762E28; web4g=!IZ0afg8pUCUOiqIgGF2t8PpmuLoYSeMA+/I5V/qvKJSHjSUN1MjExgmxBvv8MGCxEtVTHMjXWC5AXYX1K1JFGJJfk8byeYq9A5P6F/0='


def insee_search_historique_commune(dep_code):
    """
    Récupère liste historiques des communes par département
    :param dep_code:
    :return:
    """
    url = "https://www.insee.fr/fr/metadonnees/historique-commune?q=*:*"

    payload = "{\"q\":\"*:*\",\"start\":0,\"sortFields\":[{\"field\":\"historique_dateEffet\",\"order\":\"desc\"}]," \
              "\"filters\":[{\"field\":\"historique_codeDepartement\",\"tag\":\"tagHistorique_codeDepartement\"," \
              "\"values\":[\""+dep_code+"\"]}],\"rows\":\"10000\",\"facetsQuery\":[]}"
    headers = {
        'Cookie': cookie,
        'Content-Type': 'application/json'
    }
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
    except requests.ConnectionError:
        print("No internet connection available.")
        return 0
    try:
        documents = response.json().get('documents', [])
        return documents
    except ValueError as e:
        print('Echec requête ', url, ' - Mettre à jour variable cookie dans ', Path(__file__).absolute())
        sys.exit()


def make_csv_commune_historique():
    """
    Génère CSV historique des changements de nom, les créations, les disparitions et les changements de département
    Source: INSEE - Historique des communes au 2021 (depuis 1943)
    Lien: https://www.insee.fr/fr/metadonnees/historique-commune?taille=100&debut=0
    :return:
    """

    if os.path.isfile(output.get('communes_historique')) is False:
        frames = []
        df_departements = pd.read_csv(output.get('departements'), dtype=object,
                                      usecols=['departement_DEP'])
        for dep in df_departements.itertuples():
            historique_dep = insee_search_historique_commune(dep_code=dep.departement_DEP)
            data = pd.json_normalize(historique_dep)
            frames.append(data)

        if len(frames):
            merge = pd.concat(frames)
            merge.to_csv(output.get('communes_historique'), index=None)


def make_csv_communes_nouvelles():
    """
    Génère CSV des communes nouvelles 2015-2020
    Source: INSEE - Communes nouvelles
    Lien: https://www.insee.fr/fr/information/2549968
    :return:
    """
    if os.path.isfile(output.get('communes_nouvelles')) is False:
        frames = []
        xls_cn = glob.glob(sources.get('communes_nouvelles') + "/*.xl*")
        cn_cols = ['DepComN', 'NomCN', 'DepComA', 'NomCA']
        for filename in xls_cn:
            year = filename.split('communes_nouvelles_')[1][:4]
            df_cn = pd.read_excel(filename, index_col=None, header=0, dtype=object, usecols=cn_cols)
            df_cn = df_cn[df_cn.DepComN.notna()]
            df_cn['annee'] = year
            frames.append(df_cn)
        if len(frames):
            merge_cn = pd.concat(frames)
            merge_cn.to_csv(output.get('communes_nouvelles'), index=None)


def say_something(message):
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)
    engine.say(message)
    engine.runAndWait()


def block_print():
    sys.stdout = open(os.devnull, 'w')


def enable_print(to_txt=False, file_txt=""):
    if to_txt & len(file_txt):
        sys.stdout = open(file_txt, 'a')
    else:
        sys.stdout = sys.__stdout__


def generate_documentation(extend_dev=False):
    """
    Génère document pdf de documentation Sitadel
    :param extend_dev:
    :return:
    """
    # Collecte des données
    current_date = datetime.today().strftime('%d/%m/%Y %H:%M')
    pdf = FPDF(orientation='portrait')
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Sitadel le " + current_date,
             ln=1, align='C')
    pdf.cell(200, 10, txt="Reprise des données de localisation",
             ln=1, align='C')
    pdf.cell(190, 10, txt="Collecte des données",
             ln=2, align='C', border=1)
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Code officiel géographique au 1er janvier 2021 - Source: INSEE", ln=1)
    pdf.image('documentation/images/insee_cog.png', x=None, y=None, w=180, h=90, type='',
              link='https://www.insee.fr/fr/information/5057840')
    pdf.set_font("Arial", "B", size=9)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(200, 10, txt='https://www.insee.fr/fr/information/5057840',
             link="https://www.insee.fr/fr/information/5057840", ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=9)
    pdf.cell(200, 5, txt="Données servant de base aux nouvelles tables ci-dessous:", ln=1)
    new_table = '- frontend_localisation_departements' + '\n'
    new_table += '- frontend_localisation_regions' + '\n'
    new_table += '- frontend_localisation_villes' + '\n' + '\n'
    pdf.multi_cell(0, 5, new_table)
    pdf.set_font("Arial", "B", size=9)
    pdf.cell(200, 5, txt="", ln=1)
    pdf.cell(200, 5, txt="Liste des communes - fronted_localisation_villes", ln=1)
    pdf.set_font("Arial", size=8)
    pdf.cell(200, 10, txt="Note: La colonne COM est le code INSEE de la commune et n'est pas unique.", ln=1)
    file = 'documentation/dataframes/cog_villes.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)

    pdf.set_font("Arial", "B", size=9)
    pdf.cell(200, 10, txt="Liste des départements - fronted_localisation_departements", ln=1)
    pdf.set_font("Arial", size=8)
    file = 'documentation/dataframes/cog_departements.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)
    pdf.set_font("Arial", "B", size=9)
    pdf.cell(200, 10, txt="Liste des régions - fronted_localisation_regions", ln=1)
    pdf.set_font("Arial", size=8)
    file = 'documentation/dataframes/cog_regions.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)

    pdf.set_font("Arial", "B", size=10)
    pdf.set_text_color(255, 0, 255)
    pdf.cell(200, 10, txt="Pour plus d'informations, voir annexes", ln=1)
    pdf.set_text_color(0, 0, 0)

    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Base officielle des codes postaux 2021 - Source: Laposte", ln=1)
    pdf.image('documentation/images/laposte_datanova.png', x=None, y=None, w=180, h=90, type='',
              link='https://datanova.laposte.fr/explore/dataset/laposte_hexasmal/information/?disjunctive.code_commune_insee&disjunctive.nom_de_la_commune&disjunctive.code_postal&disjunctive.ligne_5')
    pdf.set_font("Arial", "B", size=9)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(200, 10, txt='https://datanova.laposte.fr/explore/dataset/laposte_hexasmal/information/....',
             link="https://datanova.laposte.fr/explore/dataset/laposte_hexasmal/information/?disjunctive.code_commune_insee&disjunctive.nom_de_la_commune&disjunctive.code_postal&disjunctive.ligne_5", ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=9)
    pdf.cell(200, 5, txt="Données servant de base à la table frontend_localisation_cp", ln=1)
    pdf.set_font("Arial", "B", size=9)
    pdf.cell(200, 5, txt="", ln=1)
    pdf.cell(200, 5, txt="Liste des codes postaux - fronted_localisation_cp", ln=1)
    pdf.set_font("Arial", size=8)
    file = 'documentation/dataframes/laposte.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)

    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Communes nouvelles - Source: INSEE", ln=1)
    pdf.image('documentation/images/insee_nouvelle_commne.png', x=None, y=None, w=180, h=70, type='',
              link='https://www.insee.fr/fr/information/2549968')
    pdf.set_font("Arial", "B", size=9)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(200, 10, txt='https://www.insee.fr/fr/information/2549968',
             link="https://www.insee.fr/fr/information/2549968", ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=9)
    pdf.cell(200, 5, txt="Données utilisées pour la reprise de données", ln=1)

    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Historique des communes - Source: INSEE", ln=1)
    pdf.image('documentation/images/insee_historique_commune.png', x=None, y=None, w=180, h=70, type='',
              link='https://www.insee.fr/en/metadonnees/historique-commune?debut=0')
    pdf.set_font("Arial", "B", size=9)
    pdf.set_text_color(0, 0, 255)
    pdf.cell(200, 10, txt='https://www.insee.fr/en/metadonnees/historique-commune?debut=0',
             link="https://www.insee.fr/en/metadonnees/historique-commune?debut=0", ln=1)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Arial", size=9)
    pdf.cell(200, 5, txt="Données utilisées pour la reprise de données", ln=1)
    #message = 'text' + '\n' + 'test asdfaf'
    #pdf.multi_cell(0, 5, message)
    pdf.output(report.get('process_pdf_method_collecte'))

    # Création des nouvelles tables
    pdf = FPDF(orientation='portrait')
    pdf.add_page()

    current_date = datetime.today().strftime('%d/%m/%Y %H:%M')
    pdf = FPDF(orientation='portrait')
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Sitadel le " + current_date,
             ln=1, align='C')
    pdf.cell(200, 10, txt="Reprise des données de localisation",
             ln=1, align='C')
    pdf.cell(190, 10, txt="Liste des nouvelles tables",
             ln=2, align='C', border=1)
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="" + '\n', ln=1)
    pdf.image('documentation/images/db/localisation_tables.png', x=None, y=None, w=180, h=35, type='')
    pdf.cell(200, 10, txt="frontend_localisation_villes", ln=1)
    pdf.image('documentation/images/db/ville.png', x=None, y=None, w=180, h=80, type='')
    pdf.set_font("Arial", size=8)
    file = 'documentation/dataframes/frontend_localisation_villes.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)

    pdf.add_page()
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="frontend_localisation_regions", ln=1)
    pdf.image('documentation/images/db/region.png', x=None, y=None, w=180, h=80, type='')
    pdf.set_font("Arial", size=8)
    file = 'documentation/dataframes/frontend_localisation_regions.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)

    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="frontend_localisation_departements", ln=1)
    pdf.image('documentation/images/db/departement.png', x=None, y=None, w=180, h=80, type='')
    pdf.cell(200, 10, txt="" + '\n' + '\n' + '\n' + '\n', ln=1)
    pdf.set_font("Arial", size=8)
    file = 'documentation/dataframes/frontend_localisation_departements.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)

    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="frontend_localisation_cp", ln=1)
    pdf.image('documentation/images/db/cp.png', x=None, y=None, w=180, h=80, type='')
    pdf.set_font("Arial", size=8)
    file = 'documentation/dataframes/frontend_localisation_cp.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)

    pdf.output(report.get('process_pdf_method_creationtable'))

    # Ajout annexe Laposte
    pdf = FPDF(orientation='portrait')
    pdf.add_page()
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Base officielle des codes postaux - Modèle de données", ln=1)
    pdf.image('documentation/laposte_cp_documentation.png', x=None, y=None, w=180, h=120, type='')
    pdf.output('documentation/laposte_cp_documentation.pdf')

    # Check reprise moa + production (check_reprise_moa_txt + check_reprise_production_txt )
    current_date = datetime.today().strftime('%d/%m/%Y %H:%M')
    pdf = FPDF(orientation='portrait')
    pdf.add_font('DejaVu', '', '/home/crxadmin/.local/share/fonts/DejaVuSansCondensed.ttf', uni=True)
    pdf.set_font('DejaVu', '', 14)
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Sitadel le " + current_date,
             ln=1, align='C')
    pdf.cell(200, 10, txt="Reprise des données de localisation",
             ln=1, align='C')
    pdf.cell(190, 10, txt="Vérification reprise de données frontend_localisation",
             ln=2, align='C', border=1)
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Environnement Moa", ln=1)
    pdf.set_font("DejaVu", size=8)
    file = 'report/reprise/check_moa.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)
    pdf.add_page()
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Environnement Production", ln=1)
    pdf.set_font("DejaVu", size=8)
    file = 'report/reprise/check_production.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)
    pdf.output('report/reprise/check_reprise_frontend_localisation.pdf')

    # Fichier table permutation
    current_date = datetime.today().strftime('%d/%m/%Y %H:%M')
    pdf = FPDF(orientation='portrait')
    pdf.add_page()
    pdf.set_font("Arial", size=10)
    pdf.cell(200, 10, txt="Sitadel le " + current_date,
             ln=1, align='C')
    pdf.cell(200, 10, txt="Reprise des données de localisation",
             ln=1, align='C')
    pdf.cell(190, 10, txt="Table de correspondance ancienne/nouvelle ville",
             ln=2, align='C', border=1)
    pdf.cell(200, 10, txt="" + '\n', ln=1)
    pdf.image('documentation/images/db/localistation_tables_repriseadded.png', x=None, y=None, w=180, h=35, type='')
    pdf.set_font("Arial", "B", size=12)
    pdf.cell(200, 10, txt="Table frontend_localisation_villes_reprise", ln=1)
    pdf.image('documentation/images/db/frontend_localisation_villes_reprise.png', x=None, y=None, w=180, h=80, type='')
    pdf.set_font("Arial", size=8)
    file = 'report/reprise/check_permutation.txt'
    f = open(file, "r")
    for x in f:
        pdf.cell(200, 4, txt=x, ln=1)
    pdf.output('report/reprise/check_permutation.pdf')

    # merge pdf
    merger = PdfFileMerger()
    merger.append(report.get('process_pdf_method_collecte'))
    merger.append(report.get('process_pdf_method_creationtable'))
    merger.append('report/reprise/check_permutation.pdf')
    if extend_dev:
        # merger.append(report.get('process_pdf_method_mysql'))
        merger.append('report/reprise/check_reprise_frontend_localisation.pdf')
    merger.append('documentation/cog_insee_doc.pdf', pages=(0, 6))
    merger.append('documentation/cog_insee_doc_modalite.pdf', pages=(1, 2))
    merger.append('documentation/laposte_cp_documentation.pdf')
    merger.write('documentation/sitadel-localisation-documentation.pdf')
    merger.close()
