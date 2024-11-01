import streamlit as st
import altair as alt
import pandas as pd

def render_bar_chart(data):
    st.subheader("Distribución de Precios por Localidad y Barrio")

    # Crear el gráfico de barras por Localidad
    st.markdown("#### Distribución de Precios por Localidad")
    localidad_data = data.groupby('locality')['price'].mean().reset_index()
    bar_chart_locality = alt.Chart(localidad_data).mark_bar().encode(
        x='price:Q',
        y='locality:N',
        tooltip=['price', 'locality']
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(bar_chart_locality, use_container_width=True)

    # Crear el gráfico de barras por Barrio
    st.markdown("#### Distribución de Precios por Barrio")
    barrio_data = data.groupby('neighbourhood')['price'].mean().reset_index()
    bar_chart_neighbourhood = alt.Chart(barrio_data).mark_bar().encode(
        x='price:Q',
        y='neighbourhood:N',
        tooltip=['price', 'neighbourhood']
    ).properties(
        width=600,
        height=400
    )
    st.altair_chart(bar_chart_neighbourhood, use_container_width=True)
