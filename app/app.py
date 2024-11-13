import streamlit as st
from components.layout.header import render_header
from components.layout.footer import render_footer
from components.layout.buttons import render_buttons
from components.layout.information import render_information
from components.graphics.bar_chart import render_bar_chart
from components.graphics.pie_chart import render_pie_chart
from components.graphics.map import display_map
from utils.scraper_utils import ejecutar_scraper  # Importar desde utils.scraper_utils
from components.graphics.data_loader import load_data  # Importar el módulo para cargar los datos
from utils.filter_options import apply_filters 


def render_page():
    # Renderizar el header
    render_header()

    # Mostrar información y botones
    render_information()
    filters = apply_filters()

    render_buttons()

    # Cargar los datos
    data = load_data(filters)

    # Mostrar gráficos
    render_bar_chart(data)
    render_pie_chart(data)
    display_map(data)

    # Renderizar el footer
    render_footer()

# Ejecutar la página
if __name__ == '__main__':
    render_page() 
    
