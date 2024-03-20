import streamlit as st

# Setting page layout
st.set_page_config(
    page_title="Admin",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Authentication ---
from helper import authentification_main
authentification_main()

# Formulaire poour uploader des poids personnalisés 
uploaded_weights = st.file_uploader("🏋️ Choisissez des poids Yolov8...",type=("pt"))

if uploaded_weights is not None:
    print(uploaded_weights)

# Menu déroulant pour choisir quel poids personnalisé utiliser


