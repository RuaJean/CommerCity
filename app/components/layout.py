import streamlit as st

def render_page():
    # Header
    st.markdown("<h1 style='text-align: center;'>Mi Aplicación Comercial</h1>", unsafe_allow_html=True)
    st.markdown("---")  # Línea divisora

    # Body
    st.subheader("Bienvenido")
    st.write("Esta es la página principal de la aplicación donde puedes encontrar información relevante.")

    st.markdown("### Información Importante:")
    st.write("- Recomendaciones personalizadas.")
    st.write("- Listado de locales comerciales disponibles.")
    st.write("- Mapas interactivos y más.")

    # Agregar algún componente interactivo básico
    st.text_input("Buscar Locales Comerciales", "")

    st.button("Buscar")

    # Footer
    st.markdown("---")
    st.markdown("<footer style='text-align: center;'>© 2024 Mi Aplicación Comercial</footer>", unsafe_allow_html=True)
