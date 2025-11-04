"""
Baixa e trata o dataset do Kaggle (Brazil Coronavirus).
"""

import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def baixar_dados_kaggle(caminho_destino="data/"):
    api = KaggleApi()
    api.authenticate()
    api.dataset_download_files('unanimad/corona-virus-brazil', path=caminho_destino, unzip=True)

def carregar_dados(caminho="data/cases-brazil-cities-time.csv"):
    df = pd.read_csv(caminho)
    df_estado = df.groupby(['date', 'state'])[['newCases', 'deaths']].sum().reset_index()
    df_estado.rename(columns={
        'date': 'data',
        'state': 'estado',
        'newCases': 'novos_casos',
        'deaths': 'obitos'
    }, inplace=True)
    return df_estado
