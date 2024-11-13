import streamlit as st
import altair as alt
import json
import pandas as pd

def render_pie_chart(data):
    st.subheader("Distribución de Locales por Vecindario")

    # Cargar el JSON con los vecindarios por localidad
    with open('data/processed/neighbourhoods_by_locality.json', 'r', encoding='utf-8') as jsonfile:
        neighbourhoods_by_locality = json.load(jsonfile)

    # Selector de localidad con un key único
    selected_locality = st.selectbox('Seleccione una localidad', options=['Todos'] + list(neighbourhoods_by_locality.keys()), key="locality_select")

    # Inicializar lista de barrios únicos
    unique_neighbourhoods = set()

    # Si se selecciona "Todos", usamos todos los vecindarios del CSV
    if selected_locality == 'Todos':
        # Recorrer todas las filas del CSV y extraer los barrios
        for neighbourhood_list in data['neighbourhood']:
            # Separar los barrios por comas y eliminar espacios en blanco
            barrios = [barrio.strip() for barrio in neighbourhood_list.split(',')]
            unique_neighbourhoods.update(barrios)  # Agregar los barrios a un conjunto para evitar duplicados
    else:
        # Obtener vecindarios del JSON según la localidad seleccionada
        unique_neighbourhoods = set(neighbourhoods_by_locality[selected_locality])

    # Crear un DataFrame con los barrios únicos y contar cuántos locales hay en cada uno
    neighbourhood_counts = {}
    for neighbourhood_list in data['neighbourhood']:
        barrios = [barrio.strip() for barrio in neighbourhood_list.split(',')]
        for barrio in barrios:
            if barrio in unique_neighbourhoods:
                if barrio not in neighbourhood_counts:
                    neighbourhood_counts[barrio] = 1
                else:
                    neighbourhood_counts[barrio] += 1

    # Convertir el diccionario de conteo a un DataFrame
    pie_chart_data = pd.DataFrame(list(neighbourhood_counts.items()), columns=['Barrio', 'count'])

    # Crear gráfico circular (Pie Chart)
    pie_chart = alt.Chart(pie_chart_data).mark_arc().encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="Barrio", type="nominal"),
        tooltip=['Barrio', 'count']
    )

    st.altair_chart(pie_chart, use_container_width=True)
