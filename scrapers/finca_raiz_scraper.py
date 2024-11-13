import requests
import json
import math

# URL de la API
url = "https://search-service.fincaraiz.com.co/api/v1/properties/search"

# Headers
headers = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "es-419,es;q=0.5",
    "Cache-Control": "no-cache",
    "Content-Type": "application/json",
    "Origin": "https://www.fincaraiz.com.co",
    "Pragma": "no-cache",
    "Referer": "https://www.fincaraiz.com.co/",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
}

# Función para realizar la solicitud y gestionar los resultados
def fetch_search_results(variables):
    print(f"\n[DEBUG] Iniciando solicitud para la página {variables['page']}...")
    
    # Crear el cuerpo de la solicitud
    body = {
        "variables": variables,
        "query": ""
    }

    # Hacer la solicitud POST
    try:
        response = requests.post(url, headers=headers, json=body)
        print(f"[DEBUG] Solicitud enviada. Estado HTTP: {response.status_code}")
    except Exception as e:
        print(f"[ERROR] Fallo en la solicitud para la página {variables['page']}: {e}")
        return {"data": [], "property": None}

    if response.status_code != 200:
        print(f"[ERROR] Error en la solicitud. Código de estado: {response.status_code}")
        print(f"[DEBUG] Respuesta de la API: {response.text}")  # Mostrar respuesta completa para depuración
        return {"data": [], "property": None}

    # Obtener los datos en formato JSON
    try:
        res = response.json()
        print(f"[DEBUG] Respuesta JSON decodificada correctamente para la página {variables['page']}.")
    except json.JSONDecodeError:
        print("[ERROR] Error al decodificar la respuesta JSON.")
        print(f"[DEBUG] Respuesta recibida: {response.text}")
        return {"data": [], "property": None}

    # Comprobar si 'hits' está en la respuesta antes de acceder
    if 'hits' not in res:
        print("[ERROR] La respuesta no contiene la clave 'hits'.")
        return {"data": [], "property": None}

    # Obtener el total de resultados
    total = res.get('hits', {}).get('total', {}).get('value', 0)
    print(f"[DEBUG] Total de resultados encontrados: {total}")
    
    results_per_page = variables.get('rows', 21)  # Usamos el valor por defecto de 21
    last_page = math.ceil(total / results_per_page)
    has_more_pages = variables.get('page', 1) < last_page
    first_item = (variables['page'] - 1) * results_per_page + 1
    last_item = min(variables['page'] * results_per_page, total)

    # Procesar los resultados y retornar
    print(f"[DEBUG] Procesando resultados de la página {variables['page']}. {len(res['hits']['hits'])} resultados obtenidos.")
    
    return {
        "property": res['hits']['hits'][0]['_source']['listing'] if res['hits']['hits'] else None,
        "searchFast": {
            "data": [hit['_source']['listing'] for hit in res['hits']['hits']],
            "paginatorInfo": {
                "currentPage": variables['page'],
                "firstItem": first_item,
                "hasMorePages": has_more_pages,
                "lastItem": last_item,
                "lastPage": last_page,
                "perPage": results_per_page,
                "total": total
            }
        }
    }

# Variables iniciales para la consulta
variables = {
    "rows": 2000,  # Resultados por página
    "page": 1,  # Página inicial
    "source": 10,  # Colocamos 'source' dentro de 'variables'
    "params": {
        "page": 1,
        "order": 2,
        "operation_type_id": 2,
        "property_type_id": [4],
        "currencyID": 4,
        "m2Currency": 4,
        "locations": [{
            "country": [{
                "name": "Colombia",
                "id": "858656c1-bbb1-4b0d-b569-f61bbdebc8f0",
                "slug": "country-48-colombia"
            }],
            "estate": {
                "name": "Bogotá, d.c.",
                "id": "2d9f0ad9-8b72-4364-a7dc-e161d7dddb4d",
                "slug": "state-colombia-11-bogota-dc"
            },
            "id": "65d441f3-a239-4111-bc5b-01c5a268869f",
            "location_point": {
                "coordinates": [-74.10969158750584, 4.656350653340584],
                "type": "point"
            },
            "name": "Bogotá",
            "slug": ["city-colombia-11-001"],
            "type": "CITY"
        }]
    }
}

# Iterar sobre las páginas y guardar los resultados 
all_results = []
current_page = 1
while True:
    print(f"\n[DEBUG] --- Iniciando proceso para la página {current_page} ---")
    variables['page'] = current_page
    result = fetch_search_results(variables)

    # Si la clave 'searchFast' no está en la respuesta, salimos del bucle
    if "searchFast" not in result or not result["searchFast"]["data"]:
        print(f"[DEBUG] No se encontraron más datos en la página {current_page}. Fin del proceso.")
        break

    all_results.extend(result["searchFast"]["data"])
    print(f"[DEBUG] Página {current_page}: {len(result['searchFast']['data'])} propiedades obtenidas.")
    
    if not result["searchFast"]["paginatorInfo"]["hasMorePages"]:
        print(f"[DEBUG] No hay más páginas disponibles después de la página {current_page}.")
        break

    current_page += 1
    

# Guardar los resultados en un archivo JSON si se obtuvieron propiedades
if all_results:
    with open('finca_raiz_properties.json', 'w', encoding='utf-8') as f:
        json.dump(all_results, f, ensure_ascii=False, indent=4)
    print(f"[DEBUG] Se han guardado {len(all_results)} propiedades en 'finca_raiz_properties.json'.")
else:
    print("[DEBUG] No se obtuvieron resultados para guardar.")
