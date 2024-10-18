import streamlit as st
import cv2
import numpy as np

# Configuração da página
st.set_page_config(
    page_title="Pole Detection App",
    page_icon="🏗️",  # Emoji de poste de eletricidade
    layout="wide",
    initial_sidebar_state="expanded"
)

# Personalização da barra lateral
st.sidebar.title("Sobre")
st.sidebar.info("Este aplicativo permite a detecção de postes de eletricidade em imagens, utilizando técnicas de aprendizado de máquina para identificar diferentes classes de tensão.")
logo = "./imgs/logo.jpg"  # Certifique-se de que o caminho do logo está correto
st.sidebar.image(logo)

# Título da página
st.title("Pole Detection")

# Descrição do aplicativo
st.markdown(
    """
    O **Pole Detection App** utiliza um modelo de aprendizado de máquina para detectar postes de eletricidade em imagens. 
    O aplicativo é capaz de identificar postes de baixa, média e alta tensão, além de extrair informações de GPS das imagens, 
    se disponíveis.
    """
)

# Instruções
st.header("Instruções")

markdown = """
1. **Carregue suas imagens**: Use a seção de upload na página de detecção para enviar suas imagens. Aceitamos formatos PNG, JPG, JPEG e WEBP.
2. **Ajuste o limite de confiança**: Utilize o controle deslizante para definir o nível de confiança desejado para a detecção de postes.
3. **Visualize os resultados**: As imagens processadas e as coordenadas GPS (se disponíveis) serão exibidas após o processamento.
4. **Salve as imagens corrigidas**: Se a detecção estiver incorreta, você pode corrigir a classe e salvar a imagem com a nova classificação.
5. **Treine o modelo com novos dados**: Você pode re-treinar o modelo com novas imagens que você classificar corretamente.
6. **Teste pela Webcam**: Use a função de detecção pela webcam para testar o modelo em tempo real. (Funcionalidade a ser implementada).
"""

st.markdown(markdown)
    
# Exemplo de imagem
st.subheader("Exemplo de Detecção")
st.image("./imgs/Low_tension_pole_3.jpg", caption="Exemplo de imagem de detecção de postes")

# Recursos do aplicativo
st.header("Recursos do Aplicativo")
st.markdown(""" 
- Detecção de postes em imagens.
- Extração de coordenadas GPS das imagens.
- Download das imagens processadas.
- Opção para corrigir a classificação e treinar o modelo com novos dados.
- Teste pela webcam. (Funcionalidade a ser implementada)
""")

# Link para o modelo Roboflow
st.header("Teste o Modelo pela Webcam")
st.markdown("[Teste o modelo pela webcam aqui](https://demo.roboflow.com/pt-2ua0w/1?publishable_key=rf_N9byBSZvx6POYi2oBOuUPx9fYRB3)")

# Contato ou suporte
st.header("Suporte")
st.markdown("""
Se você tiver dúvidas ou precisar de suporte, entre em contato pelo e-mail: 
**poledetectionteams@gmail.com**.
""")