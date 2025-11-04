"""
Módulo base do Blockchain PoA adaptado para dados de saúde.
"""

import hashlib
import pandas as pd
from datetime import datetime

def gerar_hash(conteudo, hash_anterior):
    return hashlib.sha256((conteudo + hash_anterior).encode()).hexdigest()

def criar_blockchain_inicial(df_eventos):
    # Gera um bloco inicial (genesis block)
    blockchain = []
    hash_anterior = "0" * 64
    for _, linha in df_eventos.iterrows():
        conteudo = f"{linha['estado']}-{linha['data']}-{linha['novos_casos']}-{linha['obitos']}"
        hash_atual = gerar_hash(conteudo, hash_anterior)
        blockchain.append({
            "estado": linha['estado'],
            "data": linha['data'],
            "novos_casos": linha['novos_casos'],
            "obitos": linha['obitos'],
            "hash_anterior": hash_anterior,
            "hash_atual": hash_atual
        })
        hash_anterior = hash_atual
    return pd.DataFrame(blockchain)
