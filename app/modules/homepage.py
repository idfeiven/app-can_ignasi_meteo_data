import pandas as pd
import streamlit as st


def get_map_data():
    #Mostrar en un mapa la ubicación de la estación
    map_data = pd.DataFrame(
        [[39.671896497843946, 2.904594786115017]],
        columns=['lat', 'lon'])
    return map_data


st.set_page_config(
    page_title="Sencelles (Ca'n Ignasi) - Estación meteorológica",
    page_icon="🌤️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Título de la aplicación
st.title("Sencelles (Ca'n Ignasi) - Estación meteorológica")

st.write("Modelo Davis Vantage Pro2")

st.markdown("## Localización estación")
map_data = get_map_data()
st.map(map_data, size = 1000, zoom = 9)

st.markdown("## Descripción")
st.write("Esta estación meteorológica se encuentra en las tierras del interior\n\
         de Mallorca, en completo suelo rústico. La estación consta de dos sensores\n\
         uno situado a 1.6 m del suelo, donde se mide temperatura, humedad y precipitación\n\
         y el otro está situado en lo alto de una terraza a unos 5 metros de altura,\n\
         donde se mide la velocidad y dirección del viento.")