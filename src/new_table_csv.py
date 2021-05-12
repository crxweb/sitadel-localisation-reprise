import pandas as pd
import datetime as dt
import os.path
from src import (
    utils,
)

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def make_csv_ville():
    """
    Génère CSV servant de base pour la table frontend_localisation_ville
    Source: INSEE - Code Officiel Géographique Communes 2021
    Lien: https://www.insee.fr/fr/information/5057840
    :return:
    """
    if os.path.isfile(utils.output.get('villes')) is False:
        df_cog = pd.read_csv(utils.sources.get('cog_communes'), dtype=object)

        [s_id, s_typecom, s_com, s_reg, s_dep, s_ctcd, s_arr, s_tncc, s_ncc, s_nccenr, s_libelle, s_can, s_comparent,
         s_datea, s_dateu] = ([] for _ in range(15))
        cpt_ville = 1
        for cog in df_cog.itertuples():
            s_id.append(cpt_ville)
            s_typecom.append(cog.TYPECOM)
            s_com.append(cog.COM)
            s_reg.append(cog.REG)
            s_dep.append(cog.DEP)
            s_ctcd.append(cog.CTCD)
            s_arr.append(cog.ARR)
            s_tncc.append(cog.TNCC)
            s_ncc.append(cog.NCC)
            s_nccenr.append(cog.NCCENR)
            s_libelle.append(cog.LIBELLE)
            s_can.append(cog.CAN)
            s_comparent.append(cog.COMPARENT)
            s_datea.append(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            s_dateu.append(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            cpt_ville += 1

        data = {
            'ville_id': s_id,
            'ville_TYPECOM': s_typecom,
            'ville_COM': s_com,
            'ville_REG': s_reg,
            'ville_DEP': s_dep,
            'ville_CTCD': s_ctcd,
            'ville_ARR': s_arr,
            'ville_TNCC': s_tncc,
            'ville_NCC': s_ncc,
            'ville_NCCENR': s_nccenr,
            'ville_LIBELLE': s_libelle,
            'ville_CAN': s_can,
            'ville_COMPARENT': s_comparent,
            'ville_dateAdded': s_datea,
            'ville_dateUpdated': s_dateu,
        }
        df = pd.DataFrame.from_dict(data)
        df.to_csv(utils.output.get('villes'), index=None)


def make_csv_cp():
    """
    Génère CSV servant de base pour la table frontend_localisation_cp
    Source: Laposte - Base officielle des codes postaux
    Lien: https://datanova.laposte.fr/explore/dataset/laposte_hexasmal/information
    :return:
    """
    if os.path.isfile(utils.output.get('cp')) is False:
        df_cp = pd.read_csv(utils.sources.get('laposte_base_officielle'), dtype=object)
        [s_id, s_insee, s_commune, s_cp, s_ligne5, s_libelle_ach, s_lat, s_lng, s_datea, s_dateu] = ([] for _ in range(10))
        cpt_cp = 1
        for cp in df_cp.itertuples():
            s_id.append(cpt_cp)
            s_insee.append(cp.Code_commune_INSEE)
            s_commune.append(cp.Nom_commune)
            s_cp.append(cp.Code_postal)
            if pd.isna(cp.Ligne_5) is not True:
                s_ligne5.append(cp.Ligne_5)
            else:
                s_ligne5.append(None)
            s_libelle_ach.append(cp.Libellé_d_acheminement)
            if pd.isna(cp.coordonnees_gps) is not True:
                s_lat.append(cp.coordonnees_gps.split(',')[0])
                s_lng.append(cp.coordonnees_gps.split(',')[1])
            else:
                s_lat.append(None)
                s_lng.append(None)
            s_datea.append(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            s_dateu.append(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            cpt_cp += 1

        data = {
            'cp_id': s_id,
            'cp_Code_commune_INSEE': s_insee,
            'cp_Nom_commune': s_commune,
            'cp_Code_postal': s_cp,
            'cp_Ligne_5': s_ligne5,
            'cp_Libelle_d_acheminement': s_libelle_ach,
            'cp_lat': s_lat,
            'cp_lng': s_lng,
            'cp_dateAdded': s_datea,
            'cp_dateUpdated': s_dateu,
        }
        df = pd.DataFrame.from_dict(data)
        df.to_csv(utils.output.get('cp'), index=None)


def make_csv_departement():
    """
    Génère CSV servant de base pour la table frontend_localisation_departements
    Source: INSEE - Code Officiel Géographique Départements 2021
    Lien: https://www.insee.fr/fr/information/5057840
    :return:
    """
    if os.path.isfile(utils.output.get('departements')) is False:
        df_dp = pd.read_csv(utils.sources.get('cog_departements'), dtype=object)
        [s_id, s_dep, s_reg, s_cheflieu, s_tncc, s_ncc, s_nccenr, s_libelle, s_datea, s_dateu] = ([] for _ in range(10))
        cpt_dep = 1
        for dp in df_dp.itertuples():
            s_id.append(cpt_dep)
            s_dep.append(dp.DEP)
            s_reg.append(dp.REG)
            s_cheflieu.append(dp.CHEFLIEU)
            s_tncc.append(dp.TNCC)
            s_ncc.append(dp.NCC)
            s_nccenr.append(dp.NCCENR)
            s_libelle.append(dp.LIBELLE)
            s_datea.append(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            s_dateu.append(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            cpt_dep += 1

        data = {
            'departement_id': s_id,
            'departement_DEP': s_dep,
            'departement_REG': s_reg,
            'departement_CHEFLIEU': s_cheflieu,
            'departement_TNCC': s_tncc,
            'departement_NCC': s_ncc,
            'departement_NCCENR': s_nccenr,
            'departement_LIBELLE': s_libelle,
            'departement_dateAdded': s_datea,
            'departement_dateUpdated': s_dateu,
        }
        df = pd.DataFrame.from_dict(data)
        df.to_csv(utils.output.get('departements'), index=None)


def make_csv_region():
    """
    Génère CSV servant de base pour la table frontend_localisation_regions
    Source: INSEE - Code Officiel Géographique Régions 2021
    Lien: https://www.insee.fr/fr/information/5057840
    :return:
    """
    if os.path.isfile(utils.output.get('regions')) is False:
        df_reg = pd.read_csv(utils.sources.get('cog_regions'), dtype=object)
        [s_id, s_reg, s_cheflieu, s_tncc, s_ncc, s_nccenr, s_libelle, s_datea, s_dateu] = ([] for _ in range(9))
        cpt_reg = 1
        for reg in df_reg.itertuples():
            s_id.append(cpt_reg)
            s_reg.append(reg.REG)
            s_cheflieu.append(reg.CHEFLIEU)
            s_tncc.append(reg.TNCC)
            s_ncc.append(reg.NCC)
            s_nccenr.append(reg.NCCENR)
            s_libelle.append(reg.LIBELLE)
            s_datea.append(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            s_dateu.append(dt.datetime.today().strftime('%Y-%m-%d %H:%M:%S'))
            cpt_reg += 1

        data = {
            'region_id': s_id,
            'region_REG': s_reg,
            'region_CHEFLIEU': s_cheflieu,
            'region_TNCC': s_tncc,
            'region_NCC': s_ncc,
            'region_NCCENR': s_nccenr,
            'region_LIBELLE': s_libelle,
            'region_dateAdded': s_datea,
            'region_dateUpdated': s_dateu,
        }
        df = pd.DataFrame.from_dict(data)
        df.to_csv(utils.output.get('regions'), index=None)