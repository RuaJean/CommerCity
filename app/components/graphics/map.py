import streamlit as st
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
import pandas as pd

# Función para formatear el precio
def format_price(price):
    if price >= 1_000_000:
        return f"${price // 1_000_000}M"
    elif price >= 1_000:
        return f"${price // 1_000}K"
    else:
        return f"${price}"

# Función para filtrar locales según las coordenadas visibles del mapa
def filter_data_by_bounds(data, bounds):
    if not bounds or 'southwest' not in bounds or 'northeast' not in bounds:
        st.write("No bounds found, returning all data")  # Depuración
        return data  # Retornar todos los datos si no hay límites

    # Obtener los límites correctos
    min_lat = bounds['southwest']['lat']
    min_lon = bounds['southwest']['lng']
    max_lat = bounds['northeast']['lat']
    max_lon = bounds['northeast']['lng']

    # Filtrar los locales por las coordenadas dentro de los límites
    filtered_data = data[(data['latitude'] >= min_lat) & (data['latitude'] <= max_lat) &
                         (data['longitude'] >= min_lon) & (data['longitude'] <= max_lon)]

    # Imprimir en pantalla los resultados filtrados
    st.write(f"Se han filtrado {len(filtered_data)} locales dentro de los límites visibles.")
    st.write(filtered_data.head())  # Muestra los primeros locales filtrados para ver que funciona correctamente

    return filtered_data

# Función para visualizar el mapa con clusters y popups
def display_map(data, max_markers=100):
    # Crear el mapa centrado en Bogotá
    m = folium.Map(location=[4.60971, -74.08175], zoom_start=12)

    # Añadir MarkerCluster
    marker_cluster = MarkerCluster().add_to(m)

    # Añadir marcadores de los locales, con un límite en el número de locales mostrados
    markers_loaded = 0
    for _, row in data.iterrows():
        if markers_loaded >= max_markers:
            break

        latitude = row['latitude']
        longitude = row['longitude']
        price = format_price(row['price'])
        title = row['title']
        address = row['address']

        # Verificar si hay imágenes y que no sean NaN
        images = row['images'] if isinstance(row['images'], str) else ''  # Evitar error en valores NaN
        first_image = images.split(', ')[0] if images else "https://via.placeholder.com/100"  # Imagen por defecto si falta

        # Añadir un popup con formato resumido
        popup_content = f"""
        <div style="text-align: center;">
            <img src="{first_image}" alt="{title}" style="width: 100px; height: 100px;"><br>
            <b>{price}</b><br>
            <b>{title}</b><br>
            {address}<br>
        </div>
        """

        # Añadir los marcadores al cluster
        if pd.notnull(latitude) and pd.notnull(longitude):
            folium.Marker(
                location=[latitude, longitude],  # Las coordenadas correctas
                popup=popup_content,
                icon=folium.Icon(icon="home", prefix="fa", color="blue")
            ).add_to(marker_cluster)

            markers_loaded += 1

    # Mostrar el mapa en Streamlit y obtener los límites del área visible
    map_data = st_folium(m, width=725, height=500)
    bounds = map_data.get('bounds')

    # Guardar los bounds en session state para retener al hacer click
    if bounds:
        st.session_state['bounds'] = bounds
        st.write(f"Límites del mapa actualizados: {bounds}")  # Depuración para ver los límites

    # Añadir estilos personalizados para el botón y el mensaje
    st.markdown("""
        <style>
        /* Botón en la parte inferior central del mapa */
        .map-button {
            position: absolute;
            bottom: 20px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background-color: #343a40;
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.2);
            border: none;
            cursor: pointer;
        }

        /* Texto en la parte superior central del mapa */
        .map-message {
            position: absolute;
            top: 10px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background-color: #343a40;
            color: white;
            padding: 10px;
            border-radius: 5px;
            box-shadow: 0px 2px 10px rgba(0,0,0,0.2);
        }

        /* Estilo para unificar ambos botones */
        button.map-button:hover {
            background-color: #495057;
        }
        </style>
    """, unsafe_allow_html=True)

    # Mostrar el número de locales que se están mostrando, en la parte superior del mapa
    st.markdown(
        f"""
        <div class="map-message">
            Mostrando {markers_loaded} propiedades de {max_markers}<br>Mueve el mapa o haz zoom para buscar más
        </div>
        """, unsafe_allow_html=True)

    return bounds

def render_page(data):
    # Mostrar el mapa inicial con los datos proporcionados
    bounds = display_map(data, max_markers=100)

    # Colocar el botón "Buscar en esta área" dentro del mapa, al final
    if st.button("Buscar en esta área", key="search_button"):
        st.write("Botón 'Buscar en esta área' presionado")  # Depuración para verificar que se presiona el botón
        if bounds:
            st.write("Actualizando la página con los locales visibles")
            visible_data = filter_data_by_bounds(data, bounds)
            render_page(visible_data)
        else:
            st.write("No se encontraron límites para filtrar los locales.")
