# CommerCity 🏙️ - Descubriendo Espacios Comerciales en Colombia

Bienvenido a **CommerCity**, la plataforma que transforma la búsqueda de locales comerciales en Colombia. Este proyecto ha sido diseñado para ayudar a empresarios, inversionistas y arrendadores a encontrar y analizar espacios comerciales en arriendo de manera eficiente, visual y accesible. 🌎

**Desarrollador**: Jean Rúa  
**Sitio Web**: [jeanrua.com](https://jeanrua.com)  
**LinkedIn**: [Jean Rúa](https://www.linkedin.com/in/jean-rua/)

---

## 📖 Descripción del Proyecto

CommerCity surge para resolver el problema de la dispersión de datos en los portales inmobiliarios de Colombia. Aprovechando técnicas de **web scraping**, **geocodificación** y análisis geoespacial, CommerCity recopila información de diferentes portales de arriendo de inmuebles, centralizándola en una única interfaz accesible. Así, los usuarios pueden explorar el mercado inmobiliario con filtros avanzados y visualizar información clave en mapas interactivos. 

Con CommerCity, explorar locales comerciales nunca fue tan fácil, intuitivo y completo. Aquí podrás filtrar propiedades según ubicación, precio, cercanía a puntos de interés y hasta comparar opciones en tiempo real.

## 🚀 Características Principales

1. **Extracción de Datos de Portales Inmobiliarios**: Información actualizada de sitios como Metrocuadrado, FincaRaiz, Properati, y más.
2. **Geocodificación y Visualización en Mapas**: Mapas interactivos que muestran locales y puntos de interés cercanos (restaurantes, bancos, transporte).
3. **Filtros y Búsqueda Avanzada**: Filtra por barrio, precio, tamaño, palabras clave en la descripción, entre otros.
4. **Comparación y Análisis**: Herramientas para comparar locales, explorar estadísticas y visualizar tendencias de precios.
5. **Integración con OpenStreetMap y Datos Locales**: Agrega capas de información geoespacial enriquecida, como equipamientos y servicios.

## 🛠️ Stack Tecnológico

- **Frontend y Backend**: Streamlit
- **Base de Datos**: PostgreSQL
- **Scraping**: Requests y BeautifulSoup
- **Manipulación de Datos**: Pandas
- **Geocodificación**: Geopy
- **Mapas y Visualización**: Folium y st.map() de Streamlit
- **Control de Versiones**: Git y GitHub


## 🚀 Instalación

1. Clona el repositorio y navega a la carpeta del proyecto:
   ``` 
   git clone https://github.com/jeanrua/commercity.git
   cd commercity
Instala las dependencias:

 
 
pip install -r requirements.txt
Configura las variables de entorno en un archivo .env.

Inicializa la base de datos en PostgreSQL:
 
-- Configuración en SQL (ver más en /db/schema.sql)
CREATE DATABASE commercity;
Ejecuta la aplicación:

streamlit run app/app.py
🤝 Colaboraciones
Contribuciones son bienvenidas para hacer de CommerCity una herramienta más robusta y completa. Si tienes ideas para nuevas funcionalidades o mejoras, ¡abre un PR!

Desarrollado con ❤️ por Jean Rúa. Para más detalles, visita jeanrua.com o conecta en LinkedIn.
