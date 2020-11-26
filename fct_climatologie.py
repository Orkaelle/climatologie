import pandas as pd
import numpy as np

import utiles

CSV_LOCAL_PATH = utiles.CSV_LOCAL_PATH


def creation_df ():

    print ('Import des données 1995 -> 2019...')
    # Import csv
    df = pd.read_csv(CSV_LOCAL_PATH, sep=',', usecols=['Region','Country','City','Month','Day','Year','AvgTemperature'])

    # Formatage de la date
    df['Date'] = pd.to_datetime(df[['Day','Month','Year']], yearfirst=True, errors='coerce')

    # Selection des colonnes interessantes
    df = df[['Date','City','Country','Region','AvgTemperature']]

    # Filtre dates
    df = df.loc[df['Date'] < '2020-01-01']

    print ('OK.\n\nGestion des doublons...')
    # Moyenne des doublons
    df = df.groupby(['City','Country','Region','Date']).mean().reset_index()

    print ('OK.\n\nGestion des manquants...')
    # Creation d'une colonne clé
    df['key'] = df['City'] + '_' + df['Date'].astype(str)
    df['raw'] = 'YES'

    # Création d'un index clé complet de combinaisons date/ville
    idxdate = pd.date_range('01-01-1995','31-12-2019').tolist()
    idxcity = df[['City','Country','Region']].drop_duplicates().values.tolist()

    idx = []
    for city in idxcity :
        for date in idxdate :
            d = date.strftime('%Y-%m-%d')
            idx.append([f'{city[0]}_{d}', date, city[0], city[1], city[2]])

    dfidx = pd.DataFrame(idx, columns=['key', 'Date', 'City','Country','Region'])

    # Fusion des index date-ville avec les données récupérées
    dfcomplete = pd.merge(dfidx, df[['key','AvgTemperature','raw']], how='left', on='key')

    # Suppression des villes avec moins de 95% de données
    dfanalysis = dfcomplete.groupby('City').apply(lambda x: x['raw'].count()/x['key'].count()*100).reset_index()
    dfanalysis = dfanalysis.round(2).sort_values(by=[0])
    dfanalysis = dfanalysis.loc[dfanalysis[0] < 95]

    missing = dfanalysis['City'].tolist()
    dfcomplete = dfcomplete[-dfcomplete['City'].isin(missing)]

    # Remplacement des NAN
    dfcomplete['AvgTemperature'].fillna(method='ffill', inplace=True)

    print ('OK.\n\nFinalisation...')
    # Suppression des colonnes desormais inutiles
    del dfcomplete['key']
    del dfcomplete['raw']

    # Conversion unité temperature
    dfcomplete['AvgTemperature'] = (dfcomplete['AvgTemperature'] - 32) * 5/9

    # Ajout colonnes mois et année
    dfcomplete['month'] = dfcomplete['Date'].dt.month
    dfcomplete['year'] = dfcomplete['Date'].dt.year
    
    print ('OK.\n\nTraitement terminé.')
    return dfcomplete
