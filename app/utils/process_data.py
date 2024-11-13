import json
import csv
import streamlit as st
import subprocess

def ejecutar_scraper():
    # Ejecutar el script finca_raiz_scraper.py
    result = subprocess.run(["python3", "scrapers/finca_raiz_scraper.py"], capture_output=True, text=True)

    # Mostrar el resultado en la app
    st.write(result.stdout)
    if result.returncode != 0:
        st.error("Error al ejecutar el scraper. Revisa la consola para más detalles.")

def ejecutar_filtrado():
    json_file = 'data/raw/finca_raiz_locales_bogota.json'  # Path to your JSON file
    csv_file = 'data/processed/finca_raiz_locales_bogota.csv'  # Output CSV path
    neighbourhood_json_file = 'data/processed/neighbourhoods_by_locality.json'  # Output JSON path

    # Fields to filter and save
    fields = [
        'title', 'price', 'admin_price', 'address', 'description', 'm2Built', 'latitude', 'longitude', 
        'owner_name', 'country', 'state', 'city', 'locality', 'neighbourhood', 
        'technicalSheet', 'facilities', 'images', 'socialMediaLinks'
    ]

    # Diccionario para almacenar vecindarios únicos agrupados por localidad
    neighbourhoods_by_locality = {}

    try:
        # Leer el archivo JSON
        with open(json_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        # Abrir el archivo CSV para escribir los resultados filtrados
        with open(csv_file, 'w', newline='', encoding='utf-8') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(fields)  # Escribir la fila de encabezado

            # Iterar sobre los datos y extraer los campos necesarios
            for listing in data:
                # Extraer vecindarios como una lista de nombres
                neighbourhoods = [nb.get('name', '') for nb in listing.get('locations', {}).get('neighbourhood', [])]

                # Extraer locality como una lista de nombres
                localities = [loc.get('name', '') for loc in listing.get('locations', {}).get('locality', [])]

                # Actualizar el diccionario con vecindarios únicos por localidad
                for locality in localities:
                    if locality not in neighbourhoods_by_locality:
                        neighbourhoods_by_locality[locality] = set()  # Usamos un set para evitar duplicados
                    neighbourhoods_by_locality[locality].update(neighbourhoods)

                # Extraer technicalSheet: mostrar campo 'text' y su correspondiente 'value'
                technical_sheet = ', '.join([f"{item['text']}: {item['value']}" 
                                             for item in listing.get('technicalSheet', []) 
                                             if item.get('value') is not None])

                row = [
                    listing.get('title', ''),  # Título de la propiedad
                    listing.get('price', {}).get('amount', ''),  # Precio
                    listing.get('commonExpenses', {}).get('amount', ''),  # Precio de administración
                    listing.get('address', ''),  # Dirección
                    listing.get('description', ''),  # Descripción
                    listing.get('m2Built', ''),  # Área construida
                    listing.get('locations', {}).get('location_point', '').split(' ')[2].strip('()'),  # Latitud
                    listing.get('locations', {}).get('location_point', '').split(' ')[1].strip('()'),  # Longitud
                    listing.get('owner', {}).get('name', ''),  # Nombre del propietario
                    listing.get('locations', {}).get('country', [{}])[0].get('name', ''),  # País
                    listing.get('locations', {}).get('state', [{}])[0].get('name', ''),  # Estado
                    listing.get('locations', {}).get('city', [{}])[0].get('name', ''),  # Ciudad
                    ', '.join(localities),  # Lista de localidades (nombre de la localidad)
                    ', '.join(neighbourhoods),  # Lista de vecindarios
                    technical_sheet,  # Ficha técnica (campo 'text' y su correspondiente 'value')
                    ', '.join([facility.get('name', '') for facility in listing.get('facilities', [])]),  # Instalaciones
                    ', '.join([img.get('image', '') for img in listing.get('images', [])]),  # Imágenes adicionales
                    ', '.join([link.get('url', '') for link in listing.get('socialMediaLinks', [])])  # Enlaces a redes sociales
                ]

                csvwriter.writerow(row)

        # Convertir los sets en listas y escribir el JSON con los vecindarios únicos por localidad
        for locality, neighbourhoods in neighbourhoods_by_locality.items():
            neighbourhoods_by_locality[locality] = list(neighbourhoods)  # Convertir set a lista

        with open(neighbourhood_json_file, 'w', encoding='utf-8') as json_outfile:
            json.dump(neighbourhoods_by_locality, json_outfile, indent=4, ensure_ascii=False)

        st.success(f"Datos filtrados guardados en {csv_file} y vecindarios únicos guardados en {neighbourhood_json_file}")

    except Exception as e:
        st.error(f"Error al filtrar los datos: {str(e)}")
