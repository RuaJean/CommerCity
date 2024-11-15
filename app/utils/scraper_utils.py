import subprocess
import streamlit as st  

def ejecutar_scraper():
    # Ejecutar el script finca_raiz_scraper.py
    result = subprocess.run(["python3", "scrapers/finca_raiz_scraper.py"], capture_output=True, text=True)

    # Mostrar el resultado en la app
    st.write(result.stdout)
    if result.returncode != 0:
        st.error("Error al ejecutar el scraper. Revisa la consola para más detalles.")
