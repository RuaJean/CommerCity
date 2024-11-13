import streamlit as st
from utils.process_data import ejecutar_filtrado, ejecutar_scraper

def render_buttons():
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Consultar"):
            st.write("Ejecutando filtrado...")
            ejecutar_filtrado()

    with col2:
        if st.button("Actualizar información"):
            st.write("Ejecutando scraper...")
            ejecutar_scraper()
