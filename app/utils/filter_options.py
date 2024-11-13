import streamlit as st
import json

def apply_filters():
    # Cargar el JSON que contiene localidades y barrios
    with open('data/processed/neighbourhoods_by_locality.json', 'r', encoding='utf-8') as jsonfile:
        neighbourhoods_by_locality = json.load(jsonfile)

    # Selector de localidad
    selected_locality = st.selectbox('Seleccione una localidad', options=['Todos'] + list(neighbourhoods_by_locality.keys()))

    # Inicializar lista de barrios dependiendo de la localidad seleccionada
    if selected_locality != 'Todos':
        available_neighbourhoods = ['Todos'] + neighbourhoods_by_locality[selected_locality]
    else:
        # Si se selecciona "Todos", combinar todos los barrios de todas las localidades
        available_neighbourhoods = ['Todos'] + [neighbourhood for locality_neighs in neighbourhoods_by_locality.values() for neighbourhood in locality_neighs]

    # Selector de barrios
    selected_neighbourhood = st.selectbox('Filtrar por barrio', options=available_neighbourhoods)

    # Filtro de precios
    price_min = st.slider('Precio mínimo', 0, 10000000, 1000000, step=500000)
    price_max = st.slider('Precio máximo', 0, 100000000, 50000000, step=500000)

    # Devolver los filtros seleccionados
    return {
        'locality': selected_locality,
        'neighbourhood': selected_neighbourhood,
        'price_min': price_min,
        'price_max': price_max
    }
