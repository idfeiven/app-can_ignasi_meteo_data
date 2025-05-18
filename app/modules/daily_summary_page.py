import os
import sys
import pandas as pd
import streamlit as st
from common import get_range_vals_for_color_norm,\
                   get_cmap,\
                   box_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from download_pws_data_weatherlink import download_data

# ------------------------------------FUNCTIONS------------------------------------

def get_today_max_data(data_current):

    cols_max = ['bar_hi', 'heat_index_hi', 'temp_hi', 'hum_hi', 'wind_speed_hi']
    daily_max_vals = pd.DataFrame(data_current[cols_max].max(), columns = ["variable"])
    idx_max = data_current[cols_max].idxmax()
    daily_max_vals["time"] = data_current.loc[idx_max, [col + "_at" for col in cols_max]].values.diagonal()
    
    return daily_max_vals


def get_today_min_data(data_current):

    cols_min = ['bar_lo', 'temp_lo', 'hum_lo']
    daily_min_vals = pd.DataFrame(data_current[cols_min].min(), columns = ["variable"])
    idx_min = data_current[cols_min].idxmin()
    daily_min_vals["time"] = data_current.loc[idx_min, [col + "_at" for col in cols_min]].values.diagonal()
    
    return daily_min_vals


def temperature_summary(todays_max, todays_min):
    st.markdown('## Temperatura')

    # datos de la estación meteorológica
    temperature_max = todays_max.loc["temp_hi"].variable
    datetime_temp_max = todays_max.loc["temp_hi"].time.strftime("%d-%m-%Y %H:%m UTC")
    temperature_min = todays_min.loc["temp_lo"].variable
    datetime_temp_min = todays_min.loc["temp_lo"].time.strftime("%d-%m-%Y %H:%m UTC")

    # Obtener colores según la paleta continua
    range_vals = get_range_vals_for_color_norm()
    color_temp_max = get_cmap(temperature_max, range_vals["temp"][0], range_vals["temp"][1], "gist_rainbow_r")
    color_temp_min = get_cmap(temperature_min, range_vals["temp"][0], range_vals["temp"][1], "gist_rainbow_r")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Temperatura máxima")
        box_temp = box_data(temperature_max, color_temp_max, unit = "°C")

    with col2:
        st.markdown("##### Fecha/hora")
        box_time = box_data(datetime_temp_max, color = None, unit = "")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("##### Temperatura mínima")
        box_temp = box_data(temperature_min, color_temp_min, unit = "°C")

    with col4:
        st.markdown("##### Fecha/hora")
        box_time = box_data(datetime_temp_min, color = None, unit = "")


def humidity_summary(todays_max, todays_min):
    st.markdown('## Humedad')

    # datos de la estación meteorológica
    hum_max = todays_max.loc["hum_hi"].variable
    datetime_hum_max = todays_max.loc["hum_hi"].time.strftime("%d-%m-%Y %H:%m UTC")
    hum_min = todays_min.loc["hum_lo"].variable
    datetime_hum_min = todays_min.loc["hum_lo"].time.strftime("%d-%m-%Y %H:%m UTC")

    # Obtener colores según la paleta continua
    range_vals = get_range_vals_for_color_norm()
    color_hum_max = get_cmap(hum_max, range_vals["hum"][0], range_vals["hum"][1], "BuPu")
    color_hum_min = get_cmap(hum_min, range_vals["hum"][0], range_vals["hum"][1], "BuPu")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Humedad máxima")
        box_hum = box_data(hum_max, color_hum_max, unit = "%")

    with col2:
        st.markdown("##### Fecha/hora")
        box_time = box_data(datetime_hum_max, color = None, unit = "")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("##### Humedad mínima")
        box_hum = box_data(hum_min, color_hum_min, unit = "%")

    with col4:
        st.markdown("##### Fecha/hora")
        box_time = box_data(datetime_hum_min, color = None, unit = "")


def pressure_summary(todays_max, todays_min):
    st.markdown('## Presión al nivel del mar')

    # datos de la estación meteorológica
    pres_max = todays_max.loc["bar_hi"].variable
    datetime_pres_max = todays_max.loc["bar_hi"].time.strftime("%d-%m-%Y %H:%m UTC")
    pres_min = todays_min.loc["bar_lo"].variable
    datetime_pres_min = todays_min.loc["bar_lo"].time.strftime("%d-%m-%Y %H:%m UTC")

    # Obtener colores según la paleta continua
    range_vals = get_range_vals_for_color_norm()
    color_pres_max = get_cmap(pres_max, range_vals["pres"][0], range_vals["pres"][1], "PuRd")
    color_pres_min = get_cmap(pres_min, range_vals["pres"][0], range_vals["pres"][1], "PuRd")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Presión al nivel del mar máxima")
        box_pres = box_data(pres_max, color_pres_max, unit = "hPa")

    with col2:
        st.markdown("##### Fecha/hora")
        box_time = box_data(datetime_pres_max, color = None, unit = "")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col3, col4 = st.columns(2)

    with col3:
        st.markdown("##### Presión al nivel del mar mínima")
        box_pres = box_data(pres_min, color_pres_min, unit = "hPa")

    with col4:
        st.markdown("##### Fecha/hora")
        box_time = box_data(datetime_pres_min, color = None, unit = "")


def wind_summary(todays_max):
    st.markdown('## Racha máxima')

    # datos de la estación meteorológica
    wind_max = todays_max.loc["wind_speed_hi"].variable
    datetime_wind_max = todays_max.loc["wind_speed_hi"].time.strftime("%d-%m-%Y %H:%m UTC")

    # Obtener colores según la paleta continua
    range_vals = get_range_vals_for_color_norm()
    color_wind_max = get_cmap(wind_max, range_vals["wind"][0], range_vals["wind"][1], "gist_ncar")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Racha máxima")
        box_temp = box_data(wind_max, color_wind_max, unit = "km/h")

    with col2:
        st.markdown("##### Fecha/hora")
        box_time = box_data(datetime_wind_max, color = None, unit = "")


# ------------------------------------MAIN------------------------------------

st.set_page_config(
    page_title="Resumen diario",
    page_icon=":bar_chart:",
    layout="wide",
)

today = pd.to_datetime("today").date().strftime("%Y-%m-%d")
tomorrow = pd.to_datetime("today").date() + pd.Timedelta("1 day")
tomorrow = tomorrow.strftime("%Y-%m-%d")

todays_data = download_data(station_name = "Sencelles (Ca'n Ignasi)",
                     start_datetime = today,
                     end_datetime = tomorrow,
                     historic = True)

todays_max = get_today_max_data(todays_data)
todays_min = get_today_min_data(todays_data)


st.title("Resumen diario")
temperature_summary(todays_max, todays_min)
humidity_summary(todays_max, todays_min)
wind_summary(todays_max)
pressure_summary(todays_max, todays_min)