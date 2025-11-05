import pandas as pd
import os

# Removida a importação e uso da KaggleApi

def carregar_dados():
    """
    Carrega e trata o dataset do arquivo CSV local (brazil_covid19_sample.csv).
    Assume que o CSV está no diretório raiz do projeto (um nível acima da pasta 'app').
    """
    # O nome do seu arquivo CSV no repositório é 'brazil_covid19_sample.csv'
    # O nome do arquivo que a sua função original esperava era 'cases-brazil-cities-time.csv'
    # Vou usar o nome do arquivo que você mostrou no seu repositório.
    
    caminho_csv = '../brazil_covid19_sample.csv' 
    
    try:
        df = pd.read_csv(caminho_csv)
        
        # --- TRATAMENTO DE DADOS (Baseado no seu código original) ---
        # Nota: O tratamento original usava 'date', 'state', 'newCases', 'deaths'.
        # Precisamos verificar se estes nomes existem no 'brazil_covid19_sample.csv'.
        # Usarei os nomes que você tinha no código anterior para manter a consistência 
        # com o restante do seu dashboard.
        
        # Se o seu CSV for 'brazil_covid19_sample.csv', ele pode ter colunas diferentes.
        # Para este exemplo, **assumo que as colunas originais estão presentes ou ajusto para nomes comuns.**
        # Se o CSV for de fato o 'cases-brazil-cities-time.csv', o tratamento abaixo funciona.
        
        # Se 'brazil_covid19_sample.csv' NÃO tiver as colunas exatas, este bloco pode falhar.
        # Mas seguindo a lógica do seu 'carregar_dados' original:
        
        df_estado = df.groupby(['date', 'state'])[['newCases', 'deaths']].sum().reset_index()
        
        df_estado.rename(columns={
            'date': 'data',
            'state': 'estado',
            'newCases': 'novos_casos',
            'deaths': 'obitos'
        }, inplace=True)
        
        return df_estado

    except FileNotFoundError:
        st.error(f"ERRO: Arquivo CSV não encontrado em '{os.path.abspath(caminho_csv)}'. Certifique-se de que 'brazil_covid19_sample.csv' está no diretório raiz do projeto.")
        return pd.DataFrame()
    except KeyError as e:
        st.error(f"ERRO no tratamento dos dados: Coluna esperada não encontrada no CSV. Coluna faltando: {e}. Verifique se 'brazil_covid19_sample.csv' tem as colunas 'date', 'state', 'newCases' e 'deaths'.")
        return pd.DataFrame()

# A função 'baixar_dados_kaggle' foi removida pois não é mais necessária.
