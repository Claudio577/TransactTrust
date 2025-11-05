"""
Dashboard Streamlit — visualização de dados e fraude de cartão de crédito com ML e Blockchain.
"""

import streamlit as st
import pandas as pd
import numpy as np
import altair as alt # Adicionei o Altair, caso queira plotar algo
from data_pipeline import carregar_dados, treinar_modelo_fraude # NOVO: Importa a função ML
from blockchain_core import criar_blockchain_inicial # Mantenha a função de blockchain

st.set_page_config(page_title="Auditoria de Transações", layout="wide")
st.title("💳 Auditoria de Transações (ML + Blockchain Demo)")

# 1. Carrega os dados
df = carregar_dados()

# 2. TREINAMENTO/CARREGAMENTO DO MODELO DE ML
# O @st.cache_resource garante que isso só rode uma vez, acelerando o dashboard.
if not df.empty:
    modelo, scaler = treinar_modelo_fraude(df)
else:
    st.error("Não foi possível carregar os dados. Verifique o 'data_pipeline.py' e a URL de origem.")
    st.stop() # Para a execução se os dados falharem

# 3. Mostra resumo
st.subheader("Amostra dos Dados Carregados")
st.dataframe(df.head())

# 4. Estatísticas básicas (ADAPTADAS PARA O DATASET DE FRAUDE)
st.subheader("Resumo Estatístico das Transações")

col_a, col_b, col_c = st.columns(3)
with col_a:
    st.metric("Total de Transações", len(df))

if 'Class' in df.columns:
    fraudes = df[df['Class'] == 1]
    
    with col_b:
        st.metric("Total de Fraudes (Class=1)", len(fraudes), delta_color="inverse")
    
    with col_c:
        st.metric("Porcentagem de Fraudes", f"{len(fraudes)/len(df)*100:.4f}%")
else:
    st.warning("A coluna 'Class' não foi encontrada para calcular a métrica de fraude.")

st.markdown("---")

## 🤖 SEÇÃO DE SIMULAÇÃO E ML
st.subheader("Simulação de Nova Transação (ML e Blockchain)")
st.info("Altere os valores de entrada abaixo. O ML classificará a transação, e o resultado será adicionado a um novo Bloco de Auditoria.")

# Usamos uma transação real (não fraude) como template para facilitar a simulação
template_transacao = df[df['Class'] == 0].sample(1, random_state=42).iloc[0]

# Cria o formulário de entrada
with st.form("simulacao_fraude"):
    
    # 1. Entradas Principais
    col1, col2 = st.columns(2)
    with col1:
        time = st.number_input("Time (Segundos desde a primeira transação)", 
                               min_value=0.0, max_value=200000.0, value=template_transacao['Time'], step=1.0)
    with col2:
        amount = st.number_input("Amount (Valor da Transação)", 
                                 min_value=0.0, max_value=2000.0, value=template_transacao['Amount'])

    st.markdown("---")
    st.markdown("**Variáveis Latentes (V-Features) - Altere com cuidado:**")
    
    # 2. Entradas de Features Latentes (V1, V2, V3 são geralmente as mais importantes)
    cols_v = st.columns(3)
    with cols_v[0]:
        v1 = st.number_input("V1", value=template_transacao['V1'], format="%.6f")
    with cols_v[1]:
        v2 = st.number_input("V2", value=template_transacao['V2'], format="%.6f")
    with cols_v[2]:
        v3 = st.number_input("V3", value=template_transacao['V3'], format="%.6f")
        
    submit_button = st.form_submit_button("Classificar e Gerar Bloco de Auditoria")

if submit_button:
    # 1. Preparar os dados de entrada
    
    # Cria uma cópia da transação modelo e a preenche com os inputs do usuário.
    # Isso garante que TODAS as 30 colunas (Time, Amount, V1-V28) necessárias para o ML existam.
    nova_transacao_dict = template_transacao.drop('Class').to_dict() 
    
    # Atualiza as colunas que o usuário alterou
    nova_transacao_dict['Time'] = time
    nova_transacao_dict['Amount'] = amount
    nova_transacao_dict['V1'] = v1
    nova_transacao_dict['V2'] = v2
    nova_transacao_dict['V3'] = v3
    
    # Transforma em DataFrame para processamento
    X_novo = pd.DataFrame([nova_transacao_dict])
    
    # 2. Classificação ML
    # Normaliza os dados usando o mesmo scaler usado no treino
    X_novo_scaled = scaler.transform(X_novo)
    
    previsao_ml = modelo.predict(X_novo_scaled)[0]
    probabilidade = modelo.predict_proba(X_novo_scaled)[0][1] # Probabilidade de ser fraude (classe 1)

    # 3. Apresentar Resultado da Classificação
    st.subheader("Resultado da Classificação ML")
    
    status_ml = "FRAUDE DETECTADA!" if previsao_ml == 1 else "TRANSAÇÃO NORMAL."
    icon = "🔴" if previsao_ml == 1 else "✅"
    
    st.markdown(f"**{icon} CLASSIFICAÇÃO ML: {status_ml}** (Probabilidade de Fraude: `{probabilidade*100:.4f}%`)")
        
    # 4. Geração do Bloco da Blockchain (Auditoria)
    st.subheader("Novo Bloco Adicionado à Blockchain")

    # Adiciona a Classificação ML (0 ou 1) como a coluna 'Class'
    X_novo['Class'] = previsao_ml 
    
    # Adiciona o restante das colunas (V4 a V28)
    # Isso é necessário porque o modelo ML treinou com todas as 30 features
    for col in df.columns:
        if col not in X_novo.columns:
             X_novo[col] = template_transacao[col] # Preenche com os valores do template
    
    # A transação simulada deve ter exatamente as mesmas colunas do DF original
    transacao_para_bloco = X_novo[df.columns] 
    
    # Usa a função blockchain_core para gerar um novo bloco de auditoria
    novo_bloco_df = criar_blockchain_inicial(transacao_para_bloco)
    st.dataframe(novo_bloco_df.head(1))
    st.success("A transação simulada e sua classificação de ML foram registradas no Bloco de Auditoria da Blockchain!")

st.markdown("---")

# 5. Gera blockchain inicial (Bloco Gênesis)
st.subheader("Blockchain de Amostra (Bloco Gênesis e primeiros blocos)")

# MANTENHA A GERAÇÃO DO BLOCO GÊNESIS
if len(df) >= 10:
    blockchain_df = criar_blockchain_inicial(df.head(10))
    st.dataframe(blockchain_df)
else:
    st.warning("Não há registros suficientes para gerar o primeiro bloco da blockchain.")
