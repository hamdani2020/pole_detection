import streamlit as st
from PIL import Image

# Configurações da página
st.set_page_config(page_title="Detecção de Postes Elétricos", layout="centered")

# Função para exibir a página de boas-vindas
def tela_boas_vindas():
    st.title("Detecção de Postes Elétricos")
    st.markdown("""
        Bem-vindo ao sistema de detecção de postes elétricos! Este sistema detecta postes em três categorias:
        - **Baixa Tensão**
        - **Média Tensão**
        - **Alta Tensão**
    """)
    if st.button("Iniciar Detecção"):
        st.session_state["iniciou"] = True
        st.session_state["tela"] = "upload_imagem"

# Função para a página de upload de imagem
def tela_upload_imagem():
    st.title("Envie uma Imagem para Detecção")
    st.markdown("""
        Faça o upload de uma imagem que contenha postes elétricos e o sistema irá classificá-los nas três categorias de tensão.
    """)
    imagem = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])
    
    if imagem is not None:
        img = Image.open(imagem)
        st.image(img, caption="Imagem enviada", use_column_width=True)
        if st.button("Carregar Imagem"):
            st.session_state["imagem"] = img
            st.session_state["tela"] = "exibir_resultados"

# Função para exibir os resultados
def tela_resultado():
    st.title("Resultado da Detecção")
    if st.session_state.get("imagem") is not None:
        st.image(st.session_state["imagem"], caption="Imagem carregada", use_column_width=True)
        # Simulação de detecção e classificação (isso pode ser substituído pelo modelo real)
        st.markdown("""
            - Postes Detectados:
            1. **Baixa Tensão**
            2. **Média Tensão**
            3. **Alta Tensão**
        """)
        if st.button("Nova Detecção"):
            st.session_state["tela"] = "upload_imagem"

# Função para exibir informações adicionais
def tela_sobre():
    st.title("Sobre")
    st.markdown("""
        - **Baixa Tensão:** Postes de baixa tensão são usados em áreas residenciais e pequenas indústrias.
        - **Média Tensão:** Postes de média tensão são comumente utilizados para distribuições de energia a distâncias maiores.
        - **Alta Tensão:** Postes de alta tensão são usados para transmissões em grandes distâncias, geralmente entre cidades.
    """)
    if st.button("Voltar"):
        st.session_state["tela"] = "boas_vindas"

# Adicionando o menu hambúrguer para navegação
def menu_hamburguer():
    with st.sidebar:
        st.header("Navegação")
        escolha = st.radio("", ["Upload de Imagem", "Resultados", "Sobre", "Home"])
        
        if escolha == "Upload de Imagem":
            st.session_state["tela"] = "upload_imagem"
        elif escolha == "Resultados":
            st.session_state["tela"] = "exibir_resultados"
        elif escolha == "Sobre":
            st.session_state["tela"] = "sobre"
        elif escolha == "Home":
            st.session_state["tela"] = "boas_vindas"
            st.session_state["iniciou"] = False  

# Controle de fluxo de telas
if "iniciou" not in st.session_state:
    st.session_state["iniciou"] = False
if "tela" not in st.session_state:
    st.session_state["tela"] = "boas_vindas"


if st.session_state["iniciou"]:
    menu_hamburguer()

# Chamando as telas de acordo com a sessão
if st.session_state["tela"] == "boas_vindas":
    tela_boas_vindas()
elif st.session_state["tela"] == "upload_imagem":
    tela_upload_imagem()
elif st.session_state["tela"] == "exibir_resultados":
    tela_resultado()
elif st.session_state["tela"] == "sobre":
    tela_sobre()
