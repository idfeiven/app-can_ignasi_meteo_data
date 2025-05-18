import os
import sys
import time
import pandas as pd
import streamlit as st

from common import get_range_vals_for_color_norm,\
                   get_cmap,\
                   box_data

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from download_pws_data_weatherlink import download_data, _check_router_ip


# ---------------------------------FUNCTIONS---------------------------------------

def current_conditions(data_current):
    st.title('Condiciones actuales')
    current_datetime = data_current["ts"].dt.strftime("%d-%m-%Y %H:%M").values.flatten()[0]
    st.text(f"Última actualización: {current_datetime} UTC")

    # datos de la estación meteorológica
    temperature = data_current["temp"].values.flatten()[0]
    humidity = data_current["hum"].values.flatten()[0]
    wind_speed = data_current["wind_speed_last"].values.flatten()[0]
    wind_dir = data_current["wind_dir_last"].values.flatten()[0]
    pressure = data_current["bar_sea_level"].values.flatten()[0]
    prec_daily = data_current["rainfall_daily_mm"].values.flatten()[0]

    # Obtener colores según la paleta continua
    range_vals = get_range_vals_for_color_norm()

    color_temp = get_cmap(temperature, range_vals["temp"][0], range_vals["temp"][1], "gist_rainbow_r")
    color_hum = get_cmap(humidity, range_vals["hum"][0], range_vals["hum"][1], "BuPu")
    color_wind = get_cmap(wind_speed, range_vals["wind"][0], range_vals["wind"][1], "gist_ncar")
    color_pres = get_cmap(pressure, range_vals["pres"][0], range_vals["pres"][1], "PuRd")
    color_prec = get_cmap(prec_daily, range_vals["prec"][0], range_vals["prec"][1], "cool")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### Temperatura")
        box_temp = box_data(temperature, color_temp, unit = "°C")

    with col2:
        st.markdown("##### Humedad")
        box_hum = box_data(humidity, color_hum, unit = "%")

    with col3:
        st.markdown("##### Lluvia diaria")
        box_rain = box_data(prec_daily, color_prec, unit = "mm")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("##### Velocidad del viento")
        box_wind = box_data(wind_speed, color_wind, unit = "km/h")

    with col5:
        st.markdown("##### Dirección del viento")
        box_dir_wind = box_data(wind_dir, color = None, unit = None, box_arrow=True)

    with col6:
        st.markdown("##### Presión al nivel del mar")
        box_pres = box_data(pressure, color_pres, unit = "hPa")


def temperature_conditions(data_current):
    st.markdown('## Temperatura actual')
    current_datetime = data_current["ts"].dt.strftime("%d-%m-%Y %H:%M").values.flatten()[0]
    st.text(f"Última actualización: {current_datetime} UTC")

    # datos de la estación meteorológica
    temperature = data_current["temp"].values.flatten()[0]
    dewpoint = data_current["dew_point"].values.flatten()[0]
    heat_index = data_current["heat_index"].values.flatten()[0]
    wind_chill = data_current["wind_chill"].values.flatten()[0]

    # Obtener colores según la paleta continua
    range_vals = get_range_vals_for_color_norm()
    color_temp = get_cmap(temperature, range_vals["temp"][0], range_vals["temp"][1], "gist_rainbow_r")
    color_dp = get_cmap(dewpoint, range_vals["temp"][0], range_vals["temp"][1], "gist_rainbow_r")
    color_hi = get_cmap(heat_index, range_vals["temp"][0], range_vals["temp"][1], "gist_rainbow_r")
    color_wc = get_cmap(wind_chill, range_vals["temp"][0], range_vals["temp"][1], "gist_rainbow_r")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("##### Temperatura")
        box_temp = box_data(temperature, color_temp, unit = "°C")

    with col2:
        st.markdown("##### Punto de rocío")
        box_dp = box_data(dewpoint, color_dp, unit = "°C")

    with col3:
        st.markdown("##### Sensación calor")
        box_hi = box_data(heat_index, color_hi, unit = "°C")

    with col4:
        st.markdown("##### Sensación frío")
        box_wc = box_data(wind_chill, color_wc, unit = "°C")


def rain_conditions(data_current):
    st.markdown('## Lluvia actual')
    current_datetime = data_current["ts"].dt.strftime("%d-%m-%Y %H:%M").values.flatten()[0]
    st.text(f"Última actualización: {current_datetime} UTC")

    # datos de la estación meteorológica
    daily_rain = data_current["rainfall_daily_mm"].values.flatten()[0]
    rain_15min = data_current["rainfall_last_15_min_mm"].values.flatten()[0]
    rain_rate_max = data_current["rain_rate_hi_mm"].values.flatten()[0]
    rain_rate_last = data_current["rain_rate_last_mm"].values.flatten()[0]
    rain_60min = data_current["rainfall_last_60_min_mm"].values.flatten()[0]
    rain_month = data_current["rainfall_monthly_mm"].values.flatten()[0]
    rain_year = data_current["rainfall_year_mm"].values.flatten()[0]

    # Obtener colores según la paleta continua
    range_vals = get_range_vals_for_color_norm()
    color_prec = get_cmap(daily_rain, range_vals["prec"][0], range_vals["prec"][1], "cool")
    color_rain_rate = get_cmap(rain_rate_max, range_vals["rain_rate"][0], range_vals["rain_rate"][1], "cool")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("##### Lluvia diaria")
        box_rain = box_data(daily_rain, color_prec, unit = "mm")

    with col2:
        st.markdown("##### Lluvia últimos 15 min.")
        color = get_cmap(rain_15min, 0.0, 60.0, "cool")
        box_rain_15min = box_data(rain_15min, color, unit = "mm")

    with col3:
        st.markdown("##### Intensidad máxima")
        box_rain_rr = box_data(rain_rate_max, color_rain_rate, unit = "mm/h")

    with col4:
        st.markdown("##### Intensidad")
        box_rain_rr = box_data(rain_rate_last, color_rain_rate, unit = "mm/h")

    col5, col6, col7 = st.columns(3)

    with col5:
        st.markdown("##### Lluvia última hora")
        color = get_cmap(rain_60min, 0.0, 180.0, "cool")
        box_rain_1h = box_data(rain_60min, color, unit = "mm")

    with col6:
        st.markdown("##### Lluvia este mes")
        color = get_cmap(rain_month, 0.0, 250.0, "cool")
        box_rain_month = box_data(rain_month, color, unit = "mm")

    with col7:
        st.markdown("##### Lluvia este año")
        color = get_cmap(rain_year, 0.0, 600.0, "cool")
        box_rain_year = box_data(rain_year, color, unit = "mm")


def pressure_conditions(data_current):
    st.markdown('## Presión atmosférica actual')
    current_datetime = data_current["ts"].dt.strftime("%d-%m-%Y %H:%M").values.flatten()[0]
    st.text(f"Última actualización: {current_datetime} UTC")

    # datos de la estación meteorológica
    pressure = data_current["bar_sea_level"].values.flatten()[0]
    pressure_abs = data_current["bar_absolute"].values.flatten()[0]
    pressure_trend = data_current["bar_trend"].values.flatten()[0]

    # Obtener colores según la paleta continua
    range_vals = get_range_vals_for_color_norm()
    color_pres = get_cmap(pressure, range_vals["pres"][0], range_vals["pres"][1], "PuRd")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### Presión barométrica")
        box_pres = box_data(pressure, color_pres, unit = "hPa")

    with col2:
        st.markdown("##### Presión absoluta")
        color = get_cmap(pressure_abs, 970.0, 1040.0)
        box_pres_abs = box_data(pressure_abs, color, unit = "hPa")

    with col3:
        st.markdown("##### Tendencia barométrica")
        box_pres_tr = box_data(pressure_trend, color = None, unit = "hPa")


def wind_conditions(data_current):
    st.markdown('## Viento actual')
    current_datetime = data_current["ts"].dt.strftime("%d-%m-%Y %H:%M").values.flatten()[0]
    st.text(f"Última actualización: {current_datetime} UTC")

    # datos de la estación meteorológica
    wind_speed = data_current["wind_speed_last"].values.flatten()[0]
    wind_dir = data_current["wind_dir_last"].values.flatten()[0]

    wind_gust_2min = data_current["wind_speed_hi_last_2_min"].values.flatten()[0]
    wind_dir_gust_2min = data_current["wind_dir_at_hi_speed_last_2_min"].values.flatten()[0]
    wind_speed_avg_2min = data_current["wind_speed_avg_last_2_min"].values.flatten()[0]
    wind_dir_avg_2min = data_current["wind_dir_scalar_avg_last_2_min"].values.flatten()[0]

    wind_gust_10min = data_current["wind_speed_hi_last_10_min"].values.flatten()[0]
    wind_dir_gust_10min = data_current["wind_dir_at_hi_speed_last_10_min"].values.flatten()[0]
    wind_speed_avg_10min = data_current["wind_speed_avg_last_10_min"].values.flatten()[0]
    wind_dir_avg_10min = data_current["wind_dir_scalar_avg_last_10_min"].values.flatten()[0]

    # Obtener colores según la paleta continua
    range_vals = get_range_vals_for_color_norm()
    color_wind = get_cmap(wind_speed, range_vals["wind"][0], range_vals["wind"][1], "gist_ncar")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Velocidad viento actual")
        box_wind = box_data(wind_speed, color_wind, unit = "km/h")

    with col2:
        st.markdown("##### Dirección viento actual")
        box_wind_dir = box_data(wind_dir, color = None, unit = "°", box_arrow=True)
    
    col3, col4, col5, col6 = st.columns(4)

    with col3:
        st.markdown("##### Velocidad media últimos 2 min.")
        color = get_cmap(wind_speed_avg_2min, 0.0, 60.0, "gist_ncar")
        box_wind = box_data(wind_speed_avg_2min, color, unit = "km/h")

    with col4:
        st.markdown("##### Racha últimos 2 min.")
        color = get_cmap(wind_gust_2min, 0.0, 60.0, "gist_ncar")
        box_wind = box_data(wind_gust_2min, color_wind, unit = "km/h")

    with col5:
        st.markdown("##### Dirección media últimos 2 min.")
        box_wind_dir = box_data(wind_dir_avg_2min, color = None, unit = "°", box_arrow=True)

    with col6:
        st.markdown("##### Dirección racha últimos 2 min.")
        box_wind_dir = box_data(wind_dir_gust_2min, color = None, unit = "°", box_arrow=True)

    col7, col8, col9, col10 = st.columns(4)

    with col7:
        st.markdown("##### Velocidad media últimos 10 min.")
        color = get_cmap(wind_speed_avg_2min, 0.0, 50.0, "gist_ncar")
        box_wind = box_data(wind_speed_avg_10min, color, unit = "km/h")

    with col8:
        st.markdown("##### Racha últimos 10 min.")
        color = get_cmap(wind_gust_10min, 0.0, 50.0, "gist_ncar")
        box_wind = box_data(wind_gust_10min, color_wind, unit = "km/h")

    with col9:
        st.markdown("##### Dirección media últimos 10 min.")
        box_wind_dir = box_data(wind_dir_avg_10min, color = None, unit = "°", box_arrow=True)

    with col10:
        st.markdown("##### Dirección racha últimos 10 min.")
        box_wind_dir = box_data(wind_dir_gust_10min, color = None, unit = "°", box_arrow=True)


# ---------------------------------------MAIN PROGRAM------------------------------------------        
st.set_page_config(page_title="Condiciones actuales", page_icon=":sunny:", layout="wide")

router_ip = _check_router_ip()
if router_ip == '192.168.1.1':
    sleep_time = 2.5
else:
    sleep_time = 60

placeholder = st.empty()
while True:
    data_current = download_data(station_name = "Sencelles (Ca'n Ignasi)",
                                 start_datetime = None,
                                 end_datetime = None,
                                 historic = False)

    
    with placeholder.container():

        current_conditions(data_current)
        pressure_conditions(data_current)
        temperature_conditions(data_current)
        rain_conditions(data_current)
        wind_conditions(data_current)

        st.write(f"Página actualizada a {pd.to_datetime("now").strftime("%d-%m-%Y %H:%M")}")
    
    time.sleep(sleep_time)