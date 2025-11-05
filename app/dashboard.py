"""
Dashboard Streamlit — visualização de dados e blockchain.
"""

import streamlit as st
import pandas as pd
from data_pipeline import carregar_dados
from blockchain_core import criar_blockchain_inicial


st.set_page_config(page_title="SmartHealth Blockchain", layout="wide")
st.title("🧬 SmartHealth Blockchain — Auditoria de Dados de Saúde")

# 1. Carrega os dados
df = carregar_dados()

# 2. Mostra resumo
st.subheader("Dados originais do Kaggle")
if not df.empty:
    st.dataframe(df.head())

    # 3. Gera blockchain inicial
    st.subheader("Blockchain gerado")
    # Verifica se há dados suficientes para criar o bloco inicial
    if len(df) >= 10:
        blockchain_df = criar_blockchain_inicial(df.head(10))
        st.dataframe(blockchain_df)
    else:
        st.warning("Não há registros suficientes para gerar o primeiro bloco da blockchain.")

    # 4. Estatísticas básicas
    st.subheader("Resumo estatístico")
    estados = df['estado'].unique()
    st.metric("Total de estados", len(estados))
    st.metric("Total de registros", len(df))
else:
    st.error("Não foi possível carregar os dados. Verifique o 'data_pipeline.py' e a localização do arquivo CSV.")
