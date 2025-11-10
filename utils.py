import streamlit as st

class PaginaBase:
    # Construtor que inicia as variáveis de configuração
    def __init__(self, titulo = "Página", arquivo_estilo = "styles.txt"):
        self.titulo = titulo
        self.configs = {
            "page_icon": "img/Icone.png",
            "layout": "wide",
            "initial_sidebar_state": "collapsed"
        }
        self.caminho_estilo = arquivo_estilo
    
    # Função que aplica as configurações de página
    def aplicar_config(self):
        st.set_page_config(
            page_icon=self.configs["page_icon"],
            layout=self.configs["layout"],
            initial_sidebar_state=self.configs["initial_sidebar_state"],
        )
    
    # Função que carrega o arquivo de estilos
    def carregar_estilos(self):
        try:
            with open(self.caminho_estilo, "r", encoding = "utf-8") as f:
                return f.read()
        except FileNotFoundError:
            st.error(f"Arquivo de estilos não encontrado: {self.caminho_estilo}")
            return ""
        
    # Função que aplica as configurações de estilo padrão 
    def aplicar_estilos(self):
        css = self.carregar_estilos()
        if css:
            st.markdown(f"<style>{css}</style>", unsafe_allow_html = True)
        
    # Função que define um tamanho dinâmico para um dataframe
    def dataframe_dinamico(self, df_pagina):
        n_linhas = len(df_pagina)  # Número de linhas
        altura_linhas = 34  # Pixels por linha
        altura_cabecalho = 50  # Altura do header + padding
        altura_dinamica = (n_linhas * altura_linhas) + altura_cabecalho
        
        # Condição que impede que dataframe seja maior do que 600 pixel
        if altura_dinamica <= 600:
            return altura_dinamica
        else:
            return 600