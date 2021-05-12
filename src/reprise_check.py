import pandas as pd
from src import (
    utils,
)
from tabulate import tabulate
from colorama import Fore, Style

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)


def check_env(env, enable_print=True, file_txt=""):
    if enable_print is False:
        utils.block_print()
    print('')
    print(Fore.BLUE + '--- VERIFICATION REPRISE DONNEES ---')
    print(Style.RESET_ALL + "\033[4m" + env + "\033[0m")
    df_new_ville = pd.read_csv(utils.output.get('villes'), low_memory=False)
    df_reprise = pd.read_csv(utils.output.get('reprise_ville'), low_memory=False)
    if env == 'MOA':
        df_loc = pd.read_csv(utils.sources.get('sitback_moa_localisation'), low_memory=False)
        df_loc_ville = pd.read_csv(utils.sources.get('sitback_moa_localisation_ville'), low_memory=False)
    else:
        df_loc = pd.read_csv(utils.sources.get('sitback_prod_localisation'), low_memory=False)
        df_loc_ville = pd.read_csv(utils.sources.get('sitback_prod_localisation_ville'), low_memory=False)
    df_loc = df_loc[df_loc.localisation_villeId.notna()]
    df_loc.info()
    [s_locid, s_oldvilleid, s_newvilleid, s_oldnccenr, s_newnccenr] = ([] for _ in range(5))
    for loc in df_loc.itertuples():
        s_locid.append(loc.localisation_id)
        s_oldvilleid.append(loc.localisation_villeId)
        old = df_loc_ville[df_loc_ville['ville_id'] == loc.localisation_villeId].iloc[0]
        s_oldnccenr.append(old.ville_NCCENR)
        search_reprise = df_reprise[
            (df_reprise['ville_id'] == old.ville_id)
            & (df_reprise['ville_newId'].notna())
        ]
        if len(search_reprise):
            new_id = search_reprise.iloc[0].ville_newId
            new = df_new_ville[df_new_ville['ville_id'] == new_id].iloc[0]
            s_newvilleid.append(new.ville_id)
            s_newnccenr.append(new.ville_NCCENR)
        else:
            s_newvilleid.append(None)
            s_newnccenr.append(None)

    df = pd.DataFrame({
        'loc_id': s_locid, 'old_villeId': s_oldvilleid, 'new_villeId': s_newvilleid,
        'old_NCCENR': s_oldnccenr, 'new_NCCENR': s_newnccenr
    })
    if env == 'MOA':
        df.to_csv(utils.output.get('check_reprise_moa'), index=None)
    else:
        df.to_csv(utils.output.get('check_reprise_production'), index=None)

    # on affiche dans la documentation que les tupple qui diffèrent
    df = df[df['old_NCCENR'] != df['new_NCCENR']]
    print(tabulate(df, headers='keys', tablefmt='psql'))
    utils.say_something(message="THE DATA RECOVERY'S CHECKING IS COMPLETE FOR" + env + "ENVIRONNEMENT")
    if enable_print is False:
        utils.enable_print(to_txt=True, file_txt=file_txt)


def check_moa(enable_print=True, file_txt=""):
    if enable_print is False:
        utils.block_print()
    print('')
    print(Fore.BLUE + '--- VERIFICATION REPRISE DONNEES ---')
    print(Style.RESET_ALL + "\033[4mMOA\033[0m")
    df_new_ville = pd.read_csv(utils.output.get('villes'), low_memory=False)
    df_reprise = pd.read_csv(utils.output.get('reprise_ville'), low_memory=False)
    df_moa_loc = pd.read_csv(utils.sources.get('sitback_moa_localisation'), low_memory=False)
    df_moa_loc = df_moa_loc[df_moa_loc.localisation_villeId.notna()]
    df_moa_loc.info()
    df_moa_loc_ville = pd.read_csv(utils.sources.get('sitback_moa_localisation_ville'), low_memory=False)
    [s_locid, s_oldvilleid, s_newvilleid, s_oldnccenr, s_newnccenr] = ([] for _ in range(5))
    for loc in df_moa_loc.itertuples():
        s_locid.append(loc.localisation_id)
        s_oldvilleid.append(loc.localisation_villeId)
        old = df_moa_loc_ville[df_moa_loc_ville['ville_id'] == loc.localisation_villeId].iloc[0]
        s_oldnccenr.append(old.ville_NCCENR)

        search_reprise = df_reprise[
            (df_reprise['ville_id'] == old.ville_id)
            & (df_reprise['ville_newId'].notna())
        ]
        if len(search_reprise):
            new_id = search_reprise.iloc[0].ville_newId
            new = df_new_ville[df_new_ville['ville_id'] == new_id].iloc[0]
            s_newvilleid.append(new.ville_id)
            s_newnccenr.append(new.ville_NCCENR)
        else:
            s_newvilleid.append(None)
            s_newnccenr.append(None)

    df = pd.DataFrame({
        'loc_id': s_locid, 'old_villeId': s_oldvilleid, 'new_villeId': s_newvilleid,
        'old_NCCENR': s_oldnccenr, 'new_NCCENR': s_newnccenr
    })
    df.to_csv(utils.output.get('check_reprise_moa'), index=None)
    # on affiche que les tupple qui diffèrent
    df = df[df['old_NCCENR'] != df['new_NCCENR']]
    print(tabulate(df, headers='keys', tablefmt='psql'))
    utils.say_something(message="THE DATA RECOVERY'S CHECKING IS COMPLETE FOR MOA ENVIRONNEMENT")
    if enable_print is False:
        utils.enable_print(to_txt=True, file_txt=file_txt)


def check_prod(enable_print=True, file_txt=""):
    if enable_print is False:
        utils.block_print()
    print('')
    print(Fore.BLUE + '--- VERIFICATION REPRISE DONNEES ---')
    print(Style.RESET_ALL + "\033[4mPRODUCTION\033[0m")
    df_new_ville = pd.read_csv(utils.output.get('villes'), low_memory=False)
    df_reprise = pd.read_csv(utils.output.get('reprise_ville'), low_memory=False)
    df_moa_loc = pd.read_csv(utils.sources.get('sitback_prod_localisation'), low_memory=False)
    df_moa_loc = df_moa_loc[df_moa_loc.localisation_villeId.notna()]
    df_moa_loc.info()
    df_moa_loc_ville = pd.read_csv(utils.sources.get('sitback_prod_localisation_ville'), low_memory=False)
    [s_locid, s_oldvilleid, s_newvilleid, s_oldnccenr, s_newnccenr] = ([] for _ in range(5))
    for loc in df_moa_loc.itertuples():
        s_locid.append(loc.localisation_id)
        s_oldvilleid.append(loc.localisation_villeId)
        old = df_moa_loc_ville[df_moa_loc_ville['ville_id'] == loc.localisation_villeId].iloc[0]
        s_oldnccenr.append(old.ville_NCCENR)

        search_reprise = df_reprise[
            (df_reprise['ville_id'] == old.ville_id)
            & (df_reprise['ville_newId'].notna())
        ]
        if len(search_reprise):
            new_id = search_reprise.iloc[0].ville_newId
            new = df_new_ville[df_new_ville['ville_id'] == new_id].iloc[0]
            s_newvilleid.append(new.ville_id)
            s_newnccenr.append(new.ville_NCCENR)
        else:
            s_newvilleid.append(None)
            s_newnccenr.append(None)

    df = pd.DataFrame({
        'loc_id': s_locid, 'old_villeId': s_oldvilleid, 'new_villeId': s_newvilleid,
        'old_NCCENR': s_oldnccenr, 'new_NCCENR': s_newnccenr
    })
    df.to_csv(utils.output.get('check_reprise_production'), index=None)
    print(tabulate(df, headers='keys', tablefmt='psql'))
    utils.say_something(message="THE DATA RECOVERY'S CHECKING IS COMPLETE FOR PRODUCTION ENVIRONNEMENT")
    if enable_print is False:
        utils.enable_print(to_txt=True, file_txt=file_txt)


def check_global(out_to_pdf=False):
    df_reprise = pd.read_csv(utils.output.get('reprise_ville'), low_memory=False)
    df_ville = pd.read_csv(utils.output.get('villes'), low_memory=False)
    [s_oldvilleid, s_newvilleid, s_oldnccenr, s_newnccenr] = ([] for _ in range(4))

    for ville in df_reprise.itertuples():
        s_oldvilleid.append(ville.ville_id)
        s_oldnccenr.append(ville.ville_NCCENR)
        if pd.notna(ville.ville_newId):
            new_ville = df_ville[df_ville.ville_id == ville.ville_newId].iloc[0]
            s_newvilleid.append(new_ville.ville_id)
            s_newnccenr.append(new_ville.ville_NCCENR)
        else:
            s_newvilleid.append(None)
            s_newnccenr.append(None)

    df = pd.DataFrame({
        'old_villeId': s_oldvilleid, 'new_villeId': s_newvilleid,
        'old_NCCENR': s_oldnccenr, 'new_NCCENR': s_newnccenr
    })
    df.to_csv(utils.output.get('check_reprise_global'), index=None)
    if out_to_pdf is False:
        print('')
        print(Style.RESET_ALL + "\033[4mfrontend_localisation_ville correspondance\033[0m")
        print(tabulate(df, headers='keys', tablefmt='psql'))
    utils.say_something(message="THE GLOBAL DATA RECOVERY'S CHECKING IS COMPLETE")


def check_noid():
    """
    df_reprise = pd.read_csv('../csv/output/reprise/frontend_localisation_villes.csv', low_memory=False)
    df_reprise = df_reprise[df_reprise['ville_newId'].isna()]
    # df_reprise = pd.read_csv(utils.output.get('reprise_ville'), low_memory=False)
    # group_nccenr = df_reprise.groupby('ville_NCCENR').size()
    group_nccenr = df_reprise.groupby('ville_NCCENR')['ville_NCCENR'].count().sort_values(ascending=True)
    print(group_nccenr)
    """

    """
    df_reprise = df_reprise[df_reprise['ville_newId'].isna()]
    df_reprise.to_csv('../csv/output/reprise/check_noid.csv', index=None)

    [s_oldvilleid, s_newvilleid, s_oldnccenr, s_newnccenr] = ([] for _ in range(4))
    for ville in df_reprise.itertuples():
        s_oldvilleid.append(ville.ville_id)
        s_oldnccenr.append(ville.ville_NCCENR)
        s_newvilleid.append(None)
        s_newnccenr.append(None)
    df = pd.DataFrame({
        'old_villeId': s_oldvilleid, 'new_villeId': s_newvilleid,
        'old_NCCENR': s_oldnccenr, 'new_NCCENR': s_newnccenr
    })
    print(tabulate(df, headers='keys', tablefmt='psql'))
    """


check_noid()
