"""
Dashboard Streamlit — visualização de dados e fraude de cartão de crédito.
"""

import streamlit as st
import pandas as pd
from data_pipeline import carregar_dados
from blockchain_core import criar_blockchain_inicial


st.set_page_config(page_title="SmartHealth Blockchain", layout="wide")
st.title("💳 Auditoria de Transações (Blockchain Demo)") # Título atualizado para refletir o novo dado

# 1. Carrega os dados
df = carregar_dados()

# 2. Mostra resumo
st.subheader("Amostra dos Dados Carregados")
if not df.empty:
    st.dataframe(df.head())

    # 3. Gera blockchain inicial
    st.subheader("Blockchain gerado")
    
    # A função de blockchain provavelmente espera dados agregados. 
    # Como os dados são transacionais, vamos passar o dataframe inteiro ou uma amostra grande.
    
    # MANTENHA esta verificação se a sua função blockchain for sensível ao tamanho, 
    # mas mude a referência para o novo tamanho de dados.
    if len(df) >= 10:
        # Ajuste: Como os dados são transacionais, passamos as primeiras 10 linhas
        blockchain_df = criar_blockchain_inicial(df.head(10))
        st.dataframe(blockchain_df)
    else:
        st.warning("Não há registros suficientes para gerar o primeiro bloco da blockchain.")

    # 4. Estatísticas básicas (ADAPTADAS PARA O DATASET DE FRAUDE)
    st.subheader("Resumo estatístico das Transações")
    
    # SUBSTITUI: df['estado'].unique() por algo relevante no novo CSV
    
    # Contagem total de transações
    st.metric("Total de Transações", len(df))
    
    # Contagem de Fraudes (assumindo que a coluna de fraude é 'Class' e '1' significa fraude)
    if 'Class' in df.columns:
        fraudes = df[df['Class'] == 1]
        st.metric("Total de Fraudes (Class=1)", len(fraudes))
        st.metric("Total de Não-Fraudes (Class=0)", len(df) - len(fraudes))
    else:
        st.warning("A coluna 'Class' não foi encontrada para calcular a métrica de fraude.")

else:
    st.error("Não foi possível carregar os dados. Verifique o 'data_pipeline.py' e a URL de origem.")
