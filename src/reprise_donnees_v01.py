import time
import pandas as pd
import unidecode
from src import (
    utils,
)
from colorama import Fore, Style


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def reprise_subset1(new_set, subset):
    print(Fore.LIGHTMAGENTA_EX + 'Reprise subset 1', "[" + str(subset.shape[0]) + " entries]", 'en cours...')
    print(Style.RESET_ALL)
    start_time = time.time()
    tt_res0, tt_res1, tt_resn = 0, 0, 0
    df_cn = pd.read_csv(utils.output.get('communes_nouvelles'), low_memory=False, dtype=object,
                        usecols=['DepComN', 'NomCN', 'DepComA', 'NomCA'])
    df_cn['NomCA'] = df_cn['NomCA'].apply(unidecode.unidecode)
    df_cn['NomCA'] = df_cn['NomCA'].str.upper()

    df_ch = pd.read_csv(utils.output.get('communes_historique'), low_memory=False, dtype=object)
    df_ch['libelleCommune'] = df_ch['libelleCommune'].apply(unidecode.unidecode)
    df_ch['libelleCommune'] = df_ch['libelleCommune'].str.upper()

    [s_id, s_insee, s_cdc, s_chef, s_reg, s_dep, s_com, s_ar, s_ct, s_tncc, s_artmaj, s_ncc, s_artmin, s_nccenr,
     s_lat, s_long, s_cp, s_datea, s_dateu, s_newid] = ([] for _ in range(20))

    for old in subset.itertuples():
        s_id.append(old.ville_id)
        s_insee.append(old.ville_INSEE)
        s_cdc.append(old.ville_CDC)
        s_chef.append(old.ville_CHEFLIEU)
        s_reg.append(old.ville_REG)
        s_dep.append(old.ville_DEP)
        s_com.append(old.ville_COM)
        s_ar.append(old.ville_AR)
        s_ct.append(old.ville_CT)
        s_tncc.append(old.ville_TNCC)
        s_artmaj.append(old.ville_ARTMAJ)
        s_ncc.append(old.ville_NCC)
        s_artmin.append(old.ville_ARTMIN)
        s_nccenr.append(old.ville_NCCENR)
        s_lat.append(old.ville_LAT)
        s_long.append(old.ville_LONG)
        s_cp.append(old.ville_CP)
        s_datea.append(old.ville_dateAdded)
        s_dateu.append(old.ville_dateUpdated)
        new_id = None
        old_insee = old.ville_INSEE
        format_insee = old_insee[1:6]
        old_nccenr = unidecode.unidecode(old.ville_NCCENR).upper()
        # print(old_insee, " | ", old_nccenr, " | ", old.ville_NCC, ' | ', format_insee)

        search_insee = new_set[new_set['ville_COM'] == format_insee]

        if search_insee.shape[0]:
            if search_insee.shape[0] > 1:
                search_nom = search_insee[search_insee.ville_NCCENR == old_nccenr]
                if len(search_nom):
                    new_id = search_nom.iloc[0].ville_id
                    tt_res1 += 1
                else:
                    search_typecom = search_insee[search_insee.ville_TYPECOM == 'COM']
                    if len(search_typecom):
                        new_id = search_typecom.iloc[0].ville_id
                        tt_res1 += 1
            else:
                new_id = search_insee.iloc[0].ville_id
                tt_res1 += 1
        else:
            # Recherche dans les nouvelles communes
            search_cn = df_cn[(df_cn.DepComA == format_insee) & (df_cn.NomCA == old_nccenr)]
            if search_cn.shape[0]:
                if search_cn.shape[0] == 1:
                    if len(new_set[new_set.ville_COM == search_cn.iloc[0].DepComN]):
                        new_id = new_set[new_set.ville_COM == search_cn.iloc[0].DepComN].iloc[0].ville_id
                        tt_res1 += 1
                    else:
                        tt_res0 += 1
                else:
                    tt_resn += 1
            else:
                # Recherche dans l'historique des communes
                search_ch = df_ch[df_ch.libelle.str.contains("("+format_insee+")", na=False, regex=False)]
                if search_ch.shape[0]:
                    available_com = new_set[new_set.ville_COM.isin(
                                    search_ch['codeCommune'].drop_duplicates().to_list())]
                    if available_com.shape[0]:
                        if available_com.shape[0] == 1:
                            new_id = available_com.iloc[0].ville_id
                            tt_res1 += 1
                        else:
                            if search_ch.shape[0] == 1:
                                new_id = new_set[new_set.ville_COM == search_ch.iloc[0].codeCommune].iloc[
                                    0].ville_id
                                tt_res1 += 1
                            else:
                                new_id = new_set[new_set.ville_COM == search_ch.iloc[0].codeCommune].iloc[
                                    0].ville_id
                                tt_res1 += 1
                    else:
                        tt_res0 += 1
                else:
                    tt_res0 += 1

        s_newid.append(new_id)

    data = {
        'ville_id': s_id,
        'ville_INSEE': s_insee,
        'ville_CDC': s_cdc,
        'ville_CHEFLIEU': s_chef,
        'ville_REG': s_reg,
        'ville_DEP': s_dep,
        'ville_COM': s_com,
        'ville_AR': s_ar,
        'ville_CT': s_ct,
        'ville_TNCC': s_tncc,
        'ville_ARTMAJ': s_artmaj,
        'ville_NCC': s_ncc,
        'ville_ARTMIN': s_artmin,
        'ville_NCCENR': s_nccenr,
        'ville_LAT': s_lat,
        'ville_LONG': s_long,
        'ville_CP': s_cp,
        'ville_dateAdded': s_datea,
        'ville_dateUpdated': s_dateu,
        'ville_newId': s_newid,
    }
    df = pd.DataFrame.from_dict(data)
    df['ville_NCCENR'] = df['ville_NCCENR'].str.replace('ç', 'Á')
    df.to_csv(utils.output.get('reprise_ville_sub1'), index=None)
    print("--- %s seconds ---" % (time.time() - start_time))
    # print('1 resultat:', tt_res1, '| plusieurs:', tt_resn, '| aucun:', tt_res0)
    df.info()
    utils.say_something(message="SCRIPT SUBSET ONE IS FINISHED, WAITING FOR SUBSET TWO (estimate to six minutes)")


def reprise_subset2(new_set, subset, subset_check):
    print('')
    print(Fore.LIGHTMAGENTA_EX + 'Reprise subset 2', "[" + str(subset.shape[0]) + " entries]", 'en cours...')
    print(Style.RESET_ALL)
    start_time = time.time()
    tt_res0, tt_res1, tt_resn = 0, 0, 0

    [s_id, s_insee, s_cdc, s_chef, s_reg, s_dep, s_com, s_ar, s_ct, s_tncc, s_artmaj, s_ncc, s_artmin, s_nccenr,
     s_lat, s_long, s_cp, s_datea, s_dateu, s_newid] = ([] for _ in range(20))

    df_ch = pd.read_csv(utils.output.get('communes_historique'), low_memory=False, dtype=object)
    df_ch['libelleCommune'] = df_ch['libelleCommune'].apply(unidecode.unidecode)
    df_ch['libelleCommune'] = df_ch['libelleCommune'].str.upper()

    for old in subset.itertuples():
        s_id.append(old.ville_id)
        s_insee.append(old.ville_INSEE)
        s_cdc.append(old.ville_CDC)
        s_chef.append(old.ville_CHEFLIEU)
        s_reg.append(old.ville_REG)
        s_dep.append(old.ville_DEP)
        s_com.append(old.ville_COM)
        s_ar.append(old.ville_AR)
        s_ct.append(old.ville_CT)
        s_tncc.append(old.ville_TNCC)
        s_artmaj.append(old.ville_ARTMAJ)
        s_ncc.append(old.ville_NCC)
        s_artmin.append(old.ville_ARTMIN)
        s_nccenr.append(old.ville_NCCENR)
        s_lat.append(old.ville_LAT)
        s_long.append(old.ville_LONG)
        s_cp.append(old.ville_CP)
        s_datea.append(old.ville_dateAdded)
        s_dateu.append(old.ville_dateUpdated)
        new_id = None
        old_nccenr = unidecode.unidecode(old.ville_NCCENR).upper()
        old_nccenr_pluriel = old_nccenr + 'S'
        old_cp = old.ville_CP
        old_dep = old_cp[0:2]
        #  print(old.ville_INSEE, '|', old_nccenr, '|', old_dep)

        search_nccenr_dep = new_set[
            (
                    (new_set['ville_NCCENR'] == old_nccenr)
                    | (new_set['ville_NCC'] == old_nccenr)
                    | (new_set['ville_LIBELLE'] == old_nccenr)
                    | (new_set['ville_LIBELLE'] == old_nccenr_pluriel)
            )
            & (new_set['ville_DEP'] == old_dep)
        ]

        if len(search_nccenr_dep):
            if len(search_nccenr_dep) == 1:
                new_id = search_nccenr_dep.iloc[0].ville_id
                tt_res1 += 1
            else:
                tt_resn += 1
        else:
            search_nccenr = new_set[
                (
                    (new_set['ville_NCCENR'] == old_nccenr)
                    | (new_set['ville_NCC'] == old_nccenr)
                    | (new_set['ville_LIBELLE'] == old_nccenr)
                    | (new_set['ville_LIBELLE'] == old_nccenr_pluriel)
                )
            ]
            if len(search_nccenr):
                if len(search_nccenr) == 1:
                    new_id = search_nccenr.iloc[0].ville_id
                    tt_res1 += 1
                else:
                    search_subset1 = subset_check[
                        (subset_check['ville_NCCENR'] == old_nccenr)
                        & (subset_check['ville_newId'].notna())
                        & (subset_check['ville_DEP'] == old_dep)
                    ]
                    if len(search_subset1):
                        if len(search_subset1) == 1:
                            new_id = search_subset1.iloc[0].ville_newId
                            tt_res1 += 1
                        else:
                            tt_resn += 1
                    else:
                        tt_resn += 1
            else:
                # Recherche dans l'historique des communes
                search_ch = df_ch[df_ch.libelleCommune == old_nccenr]
                if search_ch.shape[0]:
                    available_com = new_set[new_set.ville_COM.isin(
                                    search_ch['codeCommune'].drop_duplicates().to_list())]
                    if available_com.shape[0]:
                        if available_com.shape[0] == 1:
                            new_id = available_com.iloc[0].ville_id
                            tt_res1 += 1
                        else:
                            if search_ch.shape[0] == 1:
                                new_id = new_set[new_set.ville_COM == search_ch.iloc[0].codeCommune].iloc[0].ville_id
                                tt_res1 += 1
                            else:
                                new_id = new_set[new_set.ville_COM == search_ch.iloc[0].codeCommune].iloc[
                                    0].ville_id
                                tt_res1 += 1
                else:
                    have_number = ''.join(filter(lambda i: i.isdigit(), old_nccenr))
                    if len(have_number):
                        number = int(have_number)
                        if number:
                            old_nccenr_nodigit = ''.join([i for i in old_nccenr if not i.isdigit()])
                            prefix = 'E' if number > 1 else 'ER'
                            arrondissement = old_nccenr_nodigit + str(number) + prefix + ' ARRONDISSEMENT'
                            search_arrondissement = new_set[
                                (
                                    (new_set['ville_NCCENR'] == arrondissement)
                                    | (new_set['ville_NCC'] == arrondissement)
                                    | (new_set['ville_LIBELLE'] == arrondissement)
                                    | (new_set['ville_LIBELLE'] == arrondissement)
                                )
                            ]
                            if len(search_arrondissement):
                                new_id = search_arrondissement.iloc[0].ville_id
                                tt_res1 += 1
                            else:
                                tt_res0 += 1
                        else:
                            tt_res0 += 1
                    else:
                        tt_res0 += 1

        s_newid.append(new_id)
    data = {
        'ville_id': s_id,
        'ville_INSEE': s_insee,
        'ville_CDC': s_cdc,
        'ville_CHEFLIEU': s_chef,
        'ville_REG': s_reg,
        'ville_DEP': s_dep,
        'ville_COM': s_com,
        'ville_AR': s_ar,
        'ville_CT': s_ct,
        'ville_TNCC': s_tncc,
        'ville_ARTMAJ': s_artmaj,
        'ville_NCC': s_ncc,
        'ville_ARTMIN': s_artmin,
        'ville_NCCENR': s_nccenr,
        'ville_LAT': s_lat,
        'ville_LONG': s_long,
        'ville_CP': s_cp,
        'ville_dateAdded': s_datea,
        'ville_dateUpdated': s_dateu,
        'ville_newId': s_newid,
    }
    df = pd.DataFrame.from_dict(data)
    df['ville_NCCENR'] = df['ville_NCCENR'].str.replace('ç', 'Á')
    df.to_csv(utils.output.get('reprise_ville_sub2'), index=None)
    print("--- %s seconds ---" % (time.time() - start_time))
    # print('1 resultat:', tt_res1, '| plusieurs:', tt_resn, '| aucun:', tt_res0)
    df.info()
    utils.say_something(message="SCRIPT SUBSET TWO IS FINISHED")


def run(enable_print=True, file_txt=""):
    if enable_print is False:
        utils.block_print()
    print(Fore.BLUE + '--- REPRISE ancienne table frontend_localisation_villes pour correspondance nouvelle table ---')
    utils.make_csv_commune_historique()
    utils.make_csv_communes_nouvelles()

    df_ville_old = pd.read_csv(utils.sources.get('sitadel_villes'), low_memory=False, dtype=object)
    df_ville_old['ville_NCCENR'] = df_ville_old['ville_NCCENR'].str.replace('Á', 'ç')

    df_ville_new = pd.read_csv(utils.output.get('villes'), low_memory=False, dtype=object,
                               usecols=['ville_NCC', 'ville_NCCENR', 'ville_LIBELLE', 'ville_DEP', 'ville_id',
                                        'ville_COM',
                                        'ville_TYPECOM'])
    df_ville_new['ville_NCCENR'] = df_ville_new['ville_NCCENR'].apply(unidecode.unidecode)
    df_ville_new['ville_NCCENR'] = df_ville_new['ville_NCCENR'].str.upper()
    df_ville_new['ville_LIBELLE'] = df_ville_new['ville_LIBELLE'].apply(unidecode.unidecode)
    df_ville_new['ville_LIBELLE'] = df_ville_new['ville_LIBELLE'].str.upper()

    subset_1 = df_ville_old[df_ville_old.ville_INSEE.str.get(0).isin(['0'])]
    subset_2 = df_ville_old[df_ville_old.ville_INSEE.str.get(0).isin(['E', 'D', 'C'])]

    # Reprise sur le 1er sous-ensemble
    reprise_subset1(subset=subset_1, new_set=df_ville_new)

    # Reprise sur le 2ème sous-ensemble
    df_reprise_sub1 = pd.read_csv(utils.output.get('reprise_ville_sub1'), low_memory=False, dtype=object)
    df_reprise_sub1['ville_NCCENR'] = df_reprise_sub1['ville_NCCENR'].apply(unidecode.unidecode)
    df_reprise_sub1['ville_NCCENR'] = df_reprise_sub1['ville_NCCENR'].str.upper()
    reprise_subset2(subset=subset_2, subset_check=df_reprise_sub1, new_set=df_ville_new)

    # Génération CSV ancienne table frontend_localisation_villes
    print('')
    print(Fore.LIGHTMAGENTA_EX + "Génération table correspondance ville_newId >> new ville_id")
    print(Style.RESET_ALL)
    df_reprise1 = pd.read_csv(utils.output.get('reprise_ville_sub1'), low_memory=False, dtype=object)
    df_reprise1['ville_id'] = df_reprise1['ville_id'].astype('int64')
    df_reprise2 = pd.read_csv(utils.output.get('reprise_ville_sub2'), low_memory=False, dtype=object)
    df_reprise2['ville_id'] = df_reprise2['ville_id'].astype('int64')
    frames = [df_reprise1, df_reprise2]
    result = pd.concat(frames)
    result = result.sort_values('ville_id')
    result.to_csv(utils.output.get('reprise_ville'), index=None)
    result.info()
    if enable_print is False:
        utils.enable_print(to_txt=True, file_txt=file_txt)
