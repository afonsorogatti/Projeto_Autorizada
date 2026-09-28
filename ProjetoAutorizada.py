import streamlit as st
import pandas as pd
import os

# --- CONFIGURAÇÃO DO CAMINHO DO ARQUIVO ---
# Como o arquivo está no seu Desktop, podemos usar o caminho completo direto
CAMINHO_EXCEL = r"Resources x Cities para Dispatch.xlsx"

@st.cache_data(ttl=600)  # Guarda os dados na memória por 10 minutos para ficar super veloz
def carregar_dados_locais():
    try:
        # Verifica se o arquivo realmente existe no caminho especificado
        if not os.path.exists(CAMINHO_EXCEL):
            st.error(f"❌ Arquivo Excel não encontrado no caminho: {CAMINHO_EXCEL}")
            return None
        
        # Lê a planilha local
        df = pd.read_excel(CAMINHO_EXCEL)
        
        # Remove espaços em branco invisíveis do nome das colunas
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        st.error(f"Erro ao ler o arquivo Excel: {e}")
        return None

# --- INTERFACE GRÁFICA STREAMLIT ---
st.title("🔍 Buscador de Empresas por Cidade")
st.write("Consulte rapidamente as informações da planilha local.")

# Carrega os dados
df_dados = carregar_dados_locais()

if df_dados is not None:
    # Campo de texto para o usuário digitar a cidade
    cidade_busca = st.text_input("Digite o nome da cidade (Ex: São Paulo):")

    if cidade_busca:
        # Coloca o termo digitado em minúsculo e remove espaços extras nas pontas
        cidade_busca_tratada = cidade_busca.strip().lower()
        
        # Cria uma busca inteligente que ignora maiúsculas/minúsculas na planilha
        # Supondo que suas colunas no Excel se chamem 'Cidade' e 'Empresa'
        df_dados['Cidade_Lower'] = df_dados['Cidade'].astype(str).str.strip().str.lower()
        
        # Filtra as linhas correspondentes
        resultado = df_dados[df_dados['Cidade_Lower'] == cidade_busca_tratada]
        
        if not resultado.empty:
            # Lista todas as empresas encontradas para aquela cidade
            empresas = resultado['Empresa'].tolist()
            
            st.success(f"📍 **Cidade encontrada!**")
            for emp in empresas:
                st.info(f"**Empresa responsável:** {emp}")
        else:
            st.warning("Nenhuma empresa localizada para esta cidade. Verifique a ortografia.")