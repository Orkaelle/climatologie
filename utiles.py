import os
import requests


# Définition des variables
DATAS_LOCAL_PATH = './DATAS/'
RAW_LOCAL_PATH = DATAS_LOCAL_PATH + 'RAW/'
CSV_LOCAL_PATH = RAW_LOCAL_PATH + 'temperatures.csv'
CURATED_LOCAL_PATH = DATAS_LOCAL_PATH + 'CURATED/'
DATASET_PATH = CURATED_LOCAL_PATH + 'dataset.csv'
URL = 'https://stdatalake009.blob.core.windows.net/public/temperatures.csv'



def check_folder ():
    PATH = [DATAS_LOCAL_PATH, RAW_LOCAL_PATH, CURATED_LOCAL_PATH]
    for p in PATH:
        if not os.path.exists(p):
            os.mkdir(p)


def ensure_data_loaded():
    '''
    Ensure if data are already loaded. Download if missing
    '''
    if os.path.exists(CSV_LOCAL_PATH) == False:
        dl_data()
    else :
        print('Datas already downloaded.')

    print ('Datas are successfully loaded.\n')


def dl_data ():
    print ('Downloading...')
    with open(CSV_LOCAL_PATH, "wb") as f:
        r = requests.get(URL)
        f.write(r.content)
    print ('Dataset dowloaded successfully.')


def loading_raw ():
    check_folder()
    ensure_data_loaded()

