# Importação das biblitotecas
import pandas as pd # -> Manipulação de dados
import plotly.express as px # -> Criação de gráficos
import streamlit as st # -> Criação fácil de aplicações web

# Função responsável pela leitura do dataframe
def leitura_dataframe():
    # Formatação dos arquivos
    pd.set_option('display.max_columns', None)

    # Leitura dos arquivos Excel
    df_relatorio_07 = pd.read_excel("Dados/GPSAmigo-Relatorio-28-07-2025.xlsx", header = 1, usecols = "A:C, E:G, K:L")
    df_relatorio_08 = pd.read_excel("Dados/GPSAmigo-Relatorio-28-08-2025.xlsx", header = 1, usecols = "A:C, E:G, K:L")

    # Junção dos arquivos em um só Dataframe
    df_relatorio_juncao = pd.concat([df_relatorio_07, df_relatorio_08], ignore_index = True)

    # Abreviação da coluna
    df_relatorio_juncao["Tipo de Solicitação"] = df_relatorio_juncao["Tipo de Solicitação"].str.replace("SERVICEDESK (CO)", "CO")

    # Criação da coluna para formatar corretamente a exibição dos valores do eixo no visual
    df_relatorio_juncao["Tipo de Solicitação Rotulo"] = df_relatorio_juncao["Tipo de Solicitação"].apply(
    # Função personalizada que insere uma quebra de linha a cada 12 caracteres, até o comprimento total da string
        lambda x: "<br>".join([str(x)[i:i+12] for i in range (0, len(str(x)), 11)])
    )

    df_relatorio_juncao["Data de abertura"] = pd.to_datetime(df_relatorio_juncao["Data de abertura"], format = "%d/%m/%Y %H:%M:%S")
    df_relatorio_juncao["Data de abertura"] = df_relatorio_juncao["Data de abertura"].dt.floor("D")
    data_min = df_relatorio_juncao["Data de abertura"].min()
    df_relatorio_juncao["Data inteiro"] = (df_relatorio_juncao["Data de abertura"] - data_min) // pd.Timedelta("1D")
    
    data_min_int = df_relatorio_juncao["Data inteiro"].min()
    data_max_int = df_relatorio_juncao["Data inteiro"].max()
    
    # Exibição do dataframe (caso necessário visualizar, apenas descomente a linha abaixo e execute via janela interativa:)
    #display(df_relatorio_juncao)
    #df_relatorio_juncao.info()
    
    return df_relatorio_juncao, data_min, data_min_int, data_max_int

df, data_min, data_min_int, data_max_int = leitura_dataframe()

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

# Título de filtros da sidebar
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

slider_data = st.sidebar.slider(
    "Selecione o intervalo de datas",
    min_value = int(data_min_int),
    max_value = int(data_max_int),
    value = (int(data_min_int), int(data_max_int))
)

data_inicio = data_min + pd.Timedelta(days = slider_data[0])
data_fim = data_min + pd.Timedelta(days = slider_data[1])

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

df_filtrado = df[(df["Data de abertura"] >= data_inicio) & (df["Data de abertura"] <= data_fim)]

# Agrupamento do dataframe para crição dos visuais, usando somente as colunas necessárias por visual
n_chamados_operador = df_filtrado.groupby("Operador")["N.º"].count().reset_index().sort_values(by = "N.º", ascending = False)
n_chamados_tipo = df_filtrado.groupby("Tipo de Solicitação Rotulo")["N.º"].count().reset_index().sort_values(by = "N.º", ascending = False)

# Listagem das colunas para definir um valor máximo para a margem dos rótulos de dados
valores_operador = n_chamados_operador["N.º"].tolist()
valores_tipo = n_chamados_tipo["N.º"].tolist()

# Lista com as opções de cores utilizadas nos gráficos
cores_gps = ['#08306b', '#2171b5', '#4292c6', '#6baed6', "#334d5a", "#66b1b1", "#666666"]

# Criação do primeiro gráfico (gráfico de rosca)
fig1 = px.pie(n_chamados_operador, names = "Operador", values = "N.º", hole = 0.5, title = "Total de Chamados", color = "Operador", color_discrete_sequence = cores_gps)

# Estilização geral do gráfico de rosca
fig1.update_layout(
    plot_bgcolor = "#ffffff",
    paper_bgcolor = "#ffffff",
    width = 420,
    height = 320,
    legend_font_size = 9,
    legend_font_color = "#605e5c",
    title = dict(font = dict(family = "Tahoma, sans-serif Bold", size = 14, color = "#252423"), x = 0.5, xanchor = "center"),
    margin = dict(t = 40, b = 20, l = 40, r = 40)
)

# Estilização dos elementos de dados do gráfico de rosca
fig1.update_traces(
    textposition = "inside",
    textinfo = "percent + value",
    textfont_family = "Segoe UI Semibold",
    textfont_size = 10,
    textfont_color = "#ffffff"
)

# Criação do segundo gráfico (gráfico de barras)
fig2 = px.bar(n_chamados_operador, y = "Operador", x = "N.º", orientation = "h", title = "Chamados por Analista", text = "N.º", color = "Operador", color_discrete_sequence = cores_gps)

# Estilização geral do gráfico de barras
fig2.update_layout(
    plot_bgcolor = "#ffffff",
    paper_bgcolor = "#ffffff",
    xaxis = dict(tickfont = dict(), range = [-10, max(valores_operador) * 1.1], showticklabels = False, showgrid = False),
    yaxis = dict(tickfont = dict(size = 8, color = "#605e5c")),
    width = 420,
    height = 320,
    xaxis_title = None,
    yaxis_title = None,
    showlegend = False,
    title = dict(font = dict(family = "Tahoma, sans-serif Bold", size = 14, color = "#252423"), x = 0.5, xanchor = "center"),
    margin = dict(t = 40, b = 30, l = 130, r = 30)
)  

# Estilização dos elementos de dados do gráfico de barras
fig2.update_traces(
    textfont = dict(size = 8, color = "#605e5c"),
    textposition = "outside"
)

# Criação do terceiro gráfico (gráfico de colunas)
fig3 = px.bar(n_chamados_tipo, x = "Tipo de Solicitação Rotulo", y = "N.º", title = "Chamados por Tipo", text = "N.º", color = "Tipo de Solicitação Rotulo", color_discrete_sequence = cores_gps)

# Estilização geral do gráfico de colunas
fig3.update_layout(
    plot_bgcolor = "#ffffff",
    paper_bgcolor = "#ffffff",
    xaxis = dict(tickfont = dict(size = 8, color = "#605e5c"), tickangle = 0, fixedrange = False),
    yaxis = dict(range = [-5, max(valores_tipo) * 1.2], showticklabels = False, showgrid = False),
    xaxis_title = None,
    yaxis_title = None,
    width = 1900,
    height = 380,
    bargap = 0.4,
    showlegend = False,
    title = dict(font = dict(family = "Tahoma, sans-serif Bold", size = 14, color = "#252423"), x = 0.23, xanchor = "center"),
    margin = dict(t = 40, l = 40, r = 40)
)  

# Estilização dos elementos de dados do gráfico de colunas
fig3.update_traces(
    textposition = "outside", 
    textfont = dict(size = 10, color = "#605e5c")
)

# Criação de variáveis que transformam o gráfico em html, tornando possível chamá-lo
graph1_html = fig1.to_html(include_plotlyjs = "cdn")
graph2_html = fig2.to_html(include_plotlyjs = "cdn")
graph3_html = fig3.to_html(include_plotlyjs = "cdn")

# Estilizando e criando os blocos que mostram a ordem dos elementos para a página web 
st.components.v1.html(
    f'''
    <div style = "display: flex; background-color: white; padding: 2dvh 0; justify-content: space-evenly; align-items: center;">
        <h1 style = "font-family: Tahoma; font-size: 2rem; color: #334d5a; text-align: left; padding: 0 5dvh;">Visão Geral - Chamados Encerrados</h1>
        <img src = "https://iberecamargo.org.br/wp-content/uploads/2018/08/grupo-gps-preto-1.png" style = "width: 12dvh; height: 6dvh;">
    </div>

    <div style = "display: flex; flex-direction: column; align-items: center;">  
        <div style = "display: flex; justify-content: space-between; margin: 5dvh 0; gap: 6dvh;">
            <div style = "width: 38dvh; border: 8px solid #ffffff; border-radius: 15px;">
                {graph1_html}
            </div>

            <div style = "width: 38dvh; border: 8px solid #ffffff; border-radius: 15px;">
                {graph2_html}
            </div>
        </div>
                
        <div style = "width: 85dvh; overflow-x: auto; border: 8px solid #fff; border-radius: 15px;">
            {graph3_html}
        </div>
    </div>
    ''', 
    height = 1100
)

# Estilização dos elementos html e streamlit da página
st.markdown(
    """
    <style>
    body {
        margin: 0;
        display: flex;
    }
    .main {
        background-color: white;
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
        padding: 7.5dvh 0;
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
    """,
    unsafe_allow_html = True
)


