import streamlit as st

#st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """

"""

st.set_page_config(
    page_title="Pole Detection App",
    page_icon="🎈",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "./imgs/logo.jpg"
st.sidebar.image(logo)

# Customize page title
st.title("Pole Detection")

st.markdown(
    """
    
    """
)

st.header("Instructions")

markdown = """

"""

st.markdown(markdown)
