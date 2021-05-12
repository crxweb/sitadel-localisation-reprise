import pandas as pd
from src import (
    utils,
    reprise_donnees,
    reprise_check
)
from tabulate import tabulate
from colorama import Fore, Style

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', None)

if False:
    df_new_ville = pd.read_csv(utils.output.get('villes'), low_memory=False, dtype=object)
    df_new_ville.info()
    df_reprise = pd.read_csv(utils.output.get('reprise_ville'), low_memory=False, dtype=object)
    df_reprise.info()
    for i in df_reprise.index:
        if pd.notna(df_reprise.at[i, 'ville_newId']):
            new_ville = df_new_ville[df_new_ville['ville_id'] == df_reprise.at[i, 'ville_newId']].iloc[0]
            if new_ville.ville_TYPECOM in ['COMA', 'COMD'] and new_ville.ville_COMPARENT is not None:
                print(new_ville.ville_COMPARENT)
                search_parent = df_new_ville[
                    (df_new_ville.ville_COM == new_ville.ville_COMPARENT)
                    & ~(df_new_ville.ville_TYPECOM.isin(['COMA', 'COMD']))
                ]
                if len(search_parent):
                    com_parent = search_parent.iloc[0]
                    df_reprise.at[i, 'ville_newId'] = com_parent.ville_id


if False:
    df_reprise = pd.read_csv(utils.output.get('reprise_ville'), low_memory=False)
    for i in df_reprise.index:
        if True:
            df_reprise.at[i, 'ville_newId'] = 12
        else:
            df.at[i, 'ville_newId'] = 13
    print(df_reprise.head(10))

if True:
    print(Fore.BLUE + '--- VERIFICATION REPRISE DONNEES ---')
    print(Style.RESET_ALL + "\033[4mPRODUCTION\033[0m")
    df_new_ville = pd.read_csv(utils.output.get('villes'), low_memory=False)
    df_cp = pd.read_csv(utils.output.get('cp'), low_memory=False)

    df_reprise = pd.read_csv(utils.output.get('reprise_ville'), low_memory=False)
    df_moa_loc = pd.read_csv(utils.sources.get('sitback_prod_localisation'), low_memory=False)
    # df_moa_loc = pd.read_csv(utils.sources.get('sitback_moa_localisation'), low_memory=False)
    df_moa_loc = df_moa_loc[df_moa_loc.localisation_villeId.notna()]
    df_moa_loc.info()
    df_moa_loc_ville = pd.read_csv(utils.sources.get('sitback_prod_localisation_ville'), low_memory=False)
    [s_locid, s_oldvilleid, s_newvilleid, s_oldnccenr, s_newnccenr, s_newtypecom, s_oldcp, s_newcp] \
        = ([] for _ in range(8))
    for loc in df_moa_loc.itertuples():
        s_locid.append(loc.localisation_id)
        s_oldvilleid.append(loc.localisation_villeId)
        old = df_moa_loc_ville[df_moa_loc_ville['ville_id'] == loc.localisation_villeId].iloc[0]
        s_oldnccenr.append(old.ville_NCCENR)
        s_oldcp.append(loc.localisation_cp)
        search_reprise = df_reprise[
            (df_reprise['ville_id'] == old.ville_id)
            & (df_reprise['ville_newId'].notna())
            ]
        if len(search_reprise):
            new_id = search_reprise.iloc[0].ville_newId
            new = df_new_ville[df_new_ville['ville_id'] == new_id].iloc[0]
            s_newvilleid.append(new.ville_id)
            s_newnccenr.append(new.ville_NCCENR)
            s_newtypecom.append(new.ville_TYPECOM)
            search_newcp = df_cp[df_cp['cp_Code_commune_INSEE'] == new.ville_COM]
            if len(search_newcp):
                s_newcp.append(search_newcp.iloc[0].cp_Code_postal)
            else:
                s_newcp.append(None)

        else:
            s_newvilleid.append(None)
            s_newnccenr.append(None)
            s_newtypecom.append(None)
            s_newcp.append(None)

    df = pd.DataFrame({
        'loc_id': s_locid, 'old_villeId': s_oldvilleid, 'new_villeId': s_newvilleid,
        'old_NCCENR': s_oldnccenr, 'new_NCCENR': s_newnccenr, 'new_TYPECOM': s_newtypecom,
        'old_CP': s_oldcp, 'new_CP': s_newcp
    })
    """
    df = df[
        (df['old_NCCENR'] != df['new_NCCENR'])
        & (df['old_CP'] != df['new_CP'])
    ]
    """
    # df = df[~df['new_TYPECOM'].isin(['ARM', 'COM'])]
    print(tabulate(df, headers='keys', tablefmt='psql'))
    utils.say_something(message="THE DATA RECOVERY'S CHECKING IS COMPLETE FOR PRODUCTION ENVIRONNEMENT")
