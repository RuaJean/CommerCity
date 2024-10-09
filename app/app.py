import streamlit as st
from components.layout import render_page

# Ejecutar la página principal
def main():
    render_page()

if __name__ == "__main__":
    st.set_page_config(page_title="Mi Aplicación Comercial", layout="wide")
    main()
