import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA STREAMLIT
# ==============================================================================
st.set_page_config(
    page_title="Afazeres & Domésticos",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Caminhos padrão do seu ambiente local
caminho_ou_arquivo = "Tabela 1.1.1.xls"

# ==============================================================================
# 2. FUNÇÕES DE LEITURA E LIMPEZA COM PANDAS
# ==============================================================================

@st.cache_data
def carregar_e_limpar_afazeres(caminho_ou_arquivo):
    if isinstance(caminho_ou_arquivo, str):
        if caminho_ou_arquivo.lower().endswith(".csv"):
            bruto = pd.read_csv(caminho_ou_arquivo, header=None)
        else:
            bruto = pd.read_excel(caminho_ou_arquivo, engine="xlrd", header=None)
    else:
        nome = caminho_ou_arquivo.name.lower()
        if nome.endswith(".csv"):
            bruto = pd.read_csv(caminho_ou_arquivo, header=None)
        elif nome.endswith(".xls"):
            bruto = pd.read_excel(caminho_ou_arquivo, engine="xlrd", header=None)
        else:
            bruto = pd.read_excel(caminho_ou_arquivo, header=None)

    df = bruto.iloc[4:39].copy()

    df.columns = [
        "uf_regiao",
        "total",
        "total_branca",
        "total_preta_parda",
        "homem_branca",
        "homem_preta_parda",
        "mulher_branca",
        "mulher_preta_parda",
    ]
    df = df.reset_index(drop=True)

    for col in df.columns[1:]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["homens_media"] = ((df["homem_branca"] + df["homem_preta_parda"]) / 2).round(2)
    df["mulheres_media"] = ((df["mulher_branca"] + df["mulher_preta_parda"]) / 2).round(2)
    df["diferenca_genero"] = (df["mulheres_media"] - df["homens_media"]).round(2)

    return df


df = carregar_e_limpar_afazeres(caminho_ou_arquivo)
st.dataframe(df)