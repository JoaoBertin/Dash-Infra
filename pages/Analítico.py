# Importação das biblitotecas
import streamlit as st
import pandas as pd
import plotly.express as px

# Função responsável pela leitura do dataframe
def leitura_dataframe():
    # Formatação dos arquivos
    pd.set_option('display.max_columns', None)

    # Leitura dos arquivos Excel
    df_relatorio_07 = pd.read_excel("Dados/GPSAmigo-Relatorio-28-07-2025.xlsx", header = 1, usecols = "A:C, E:G, K:L")
    df_relatorio_08 = pd.read_excel("Dados/GPSAmigo-Relatorio-28-08-2025.xlsx", header = 1, usecols = "A:C, E:G, K:L")

    # Junção dos arquivos em um só Dataframe
    df_relatorio_juncao = pd.concat([df_relatorio_07, df_relatorio_08], ignore_index = True)

    # Exibição do dataframe (caso necessário visualizar, apenas descomente a linha abaixo e execute via janela interativa:)
    #display(df_relatorio_juncao)
    
    return df_relatorio_juncao

df = leitura_dataframe()

# Configuraçãos gerais da página streamlit
st.set_page_config(
    page_icon = "Imagens/Icone.png",
    layout = "wide",
    initial_sidebar_state = "collapsed",
)

# Unificação dos valores disponíveis na coluna para criação das opções dos filtros
opcoes_filtro1 = df["Área Solicitante"].unique()
opcoes_filtro2 = df["Contato"].unique()
opcoes_filtro3 = df["Operador"].unique()
opcoes_filtro4 = df["Regional"].unique()
opcoes_filtro5 = df["Tipo de Solicitação"].unique()

# Título da sidebar
st.sidebar.header("Filtros")

# Criação das caixas de filtros
filtro1 = st.sidebar.multiselect(
    "ÁREA SOLICITANTE",
    options = opcoes_filtro1,
    placeholder = "Todos"
    )

filtro2 = st.sidebar.multiselect(
    "CONTATO",
    options = opcoes_filtro2,
    placeholder = "Todos"
    )

filtro3 = st.sidebar.multiselect(
    "OPERADOR",
    options = opcoes_filtro3,
    placeholder = "Todos"
    )

filtro4 = st.sidebar.multiselect(
    "REGIONAL",
    options = opcoes_filtro4,
    placeholder = "Todos"
    )

filtro5 = st.sidebar.multiselect(
    "TIPO DE SOLICITAÇÃO",
    options = opcoes_filtro5,
    placeholder = "Todos"
    )

# Título de datas da sidebar
st.sidebar.header("Datas")

# Cópia do dataframe original para aplicar os filtros
df_filtrado = df.copy()

# Aplicação da condicional dos filtros
if filtro1:
    df_filtrado = df_filtrado[df_filtrado["Área Solicitante"].isin(filtro1)]
if filtro2:
    df_filtrado = df_filtrado[df_filtrado["Contato"].isin(filtro2)]
if filtro3:
    df_filtrado = df_filtrado[df_filtrado["Operador"].isin(filtro3)]
if filtro4:
    df_filtrado = df_filtrado[df_filtrado["Regional"].isin(filtro4)]
if filtro5:
    df_filtrado = df_filtrado[df_filtrado["Tipo de Solicitação"].isin(filtro5)]

# Estilizando e criando os blocos da página web 
st.markdown(
    '''
    <div style="display: flex; background-color: white; padding: 2dvh 0; justify-content: space-evenly; align-items: center; margin-bottom: 6dvh;">
        <h1 style="font-family: Tahoma; font-size: 2rem; color: #334d5a; text-align: left; padding: 7dvh 0;"></h1>
        <img src="https://iberecamargo.org.br/wp-content/uploads/2018/08/grupo-gps-preto-1.png" style="width: 24dvh; height: 12dvh;">
    </div>

    <style>
    body {
        margin: 0;
        display: flex;
    }
    .main {
        background-color: #ffffff;
        padding: 0;
        margin: 0;
        color: #605e5c;
    }
    /* Container principal */
    .block-container {
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        background-color: #b3b3b3;
        padding: 10dvh 0;
        margin: 0;
        max-width: 100%;
    }
    /* Sidebar */
    .st-emotion-cache-1lqf7hx  {
        background-color: #ffffff;
        color: #605e5c;
        padding-left: 0;
        padding-right: 0;
        border: 2px solid #b3b3b3;
    }
    /* Seta de fechar do sidebar */
    .st-emotion-cache-1lqf7hx span {
        color: #252423;
    }
    /* Caixa de filtros do sidebar */
    div[data-baseweb="select"] > div {
        background-color: #ffffff;
        border: 2px solid #b3b3b3;
        border-radius: 8px;
        font-size: 16px;
    }
    /* Filtros selecionados */
    div[data-baseweb="select"] span {
        background-color: #334d5a;
        color: #ffffff;
        border-radius: 12px;
    }
    /* Título das caixas de filtro */
    .st-emotion-cache-1891hll {
        font-family: "Source Sans";
        padding-left: 1dvh;
        color: #252423;
    }
    /* Fonte das caixas de filtro */
    .st-ce {
        color: #b3b3b3;
    }
    /* Fonte das caixas de filtro */
    .st-cy {
        color: #b3b3b3;
    }
    /* Texto da caixa de seleção dos filtros */
    .st-b6 {
        color: #605e5c;
    }
    /* Fundo da caixa de seleção dos filtros */
    .st-b6 ul {
        background-color: #ffffff;
    }
    <style>
    ''', unsafe_allow_html=True
)

# Criação da estrutura de colunas do próprio streamlit
col1, col2, col3 = st.columns([1, 16, 1])

# Preenche as colunas 1 e 3 com conteúdo vazio, para a criação de margens do dataframe do analítico
with col1:
    st.empty()

# Exibe o dataframe   
with col2:
    st.dataframe(df_filtrado.style, height = 600, width = "stretch")
    
with col3:
    st.empty()

