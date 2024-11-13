import pandas as pd
import streamlit as st

@st.cache_data
def load_data(filters=None):
    """
    Cargar los datos desde un archivo CSV, y si se pasan filtros, aplicarlos.
    """
    # Ruta al archivo CSV
    csv_path = 'data/processed/finca_raiz_locales_bogota.csv'

    try:
        # Cargar los datos del CSV
        data = pd.read_csv(csv_path)
        
        # Aplicar los filtros si existen
        if filters:
            if 'neighbourhood' in filters and filters['neighbourhood'] != 'Todos':
                data = data[data['neighbourhood'] == filters['neighbourhood']]
            if 'price_min' in filters and 'price_max' in filters:
                data = data[(data['price'] >= filters['price_min']) & (data['price'] <= filters['price_max'])]

        return data
    except FileNotFoundError:
        st.error("Archivo de datos no encontrado.")
        return pd.DataFrame()  # Retorna un DataFrame vacío si el archivo no se encuentra
