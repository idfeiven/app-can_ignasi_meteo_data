import os
import sys
import time
import matplotlib
import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from download_pws_data_weatherlink import download_current_data


# ---------------------------------CONFIG-----------------------------------------
# Rango de valores para normalizar colores
temp_min, temp_max = -10, 45
hum_min, hum_max = 0, 100
wind_min, wind_max = 0, 100
pres_min, pres_max = 980, 1050
prec_min, prec_max = 0, 200
rain_rate_min, rain_rate_max = 0, 1440

# ---------------------------------FUNCTIONS---------------------------------------

def _get_cmap(valor, min_val, max_val, cmap_name="coolwarm"):
    norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
    cmap = matplotlib.colormaps.get_cmap(cmap_name)
    color_rgb = cmap(norm(valor))[:3]  # Obtiene el color en formato RGB
    color_hex = mcolors.rgb2hex(color_rgb)  # Convierte a HEX
    return color_hex  # Lo convertimos a formato HEX


def _box_data(data, color, unit, box_arrow = False):
    '''
    Creates a default box data filled with color
    '''

    if box_arrow == True:
        box = st.markdown(f"""
            <style>
                .wind-box {{
                    background-color: #827e7e;
                    padding: 10px;
                    border-radius: 10px;
                    text-align: center;
                    width: 150px;
                    display: inline-block;
                    margin: 10px;
                }}
                .wind-arrow {{
                    font-size: 100px;
                    display: inline-block;
                    transform: rotate({data}deg);
                    transition: transform 0.5s ease-in-out;
                }}
            </style>

            <div class="wind-box">
                <h2 class="wind-arrow">&#8595</h2>  <!-- Flecha que rota -->
                <h2>{data}°</h2>
            </div>
            """, unsafe_allow_html=True)
    elif color:
        box = st.markdown(f"<div style='background-color:{color};padding:10px;border-radius:10px;'><h2>{data} {unit}</h2></div>", unsafe_allow_html=True)
    else:
        box = st.markdown(f"<div style=padding:10px;border-radius:10px;'><h2>{data} {unit}</h2></div>", unsafe_allow_html=True)

    return box


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
    color_temp = _get_cmap(temperature, temp_min, temp_max, "jet")
    color_hum = _get_cmap(humidity, hum_min, hum_max, "BuPu")
    color_wind = _get_cmap(wind_speed, wind_min, wind_max, "gist_ncar")
    color_pres = _get_cmap(pressure, pres_min, pres_max, "PuRd")
    color_prec = _get_cmap(prec_daily, prec_min, prec_max, "cool")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### Temperatura")
        box_temp = _box_data(temperature, color_temp, unit = "°C")

    with col2:
        st.markdown("##### Humedad")
        box_hum = _box_data(humidity, color_hum, unit = "%")

    with col3:
        st.markdown("##### Lluvia diaria")
        box_rain = _box_data(prec_daily, color_prec, unit = "mm")

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("##### Velocidad del viento")
        box_wind = _box_data(wind_speed, color_wind, unit = "km/h")

    with col5:
        st.markdown("##### Dirección del viento")
        box_dir_wind = _box_data(wind_dir, color = None, unit = None, box_arrow=True)

    with col6:
        st.markdown("##### Presión al nivel del mar")
        box_pres = _box_data(pressure, color_pres, unit = "hPa")


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
    color_temp = _get_cmap(temperature, temp_min, temp_max, "jet")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("##### Temperatura")
        box_temp = _box_data(temperature, color_temp, unit = "°C")

    with col2:
        st.markdown("##### Punto de rocío")
        box_dp = _box_data(dewpoint, color_temp, unit = "°C")

    with col3:
        st.markdown("##### Sensación calor")
        box_hi = _box_data(heat_index, color_temp, unit = "°C")

    with col4:
        st.markdown("##### Sensación frío")
        box_wc = _box_data(wind_chill, color_temp, unit = "°C")


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
    color_prec = _get_cmap(daily_rain, prec_min, prec_max, "cool")
    color_rain_rate = _get_cmap(rain_rate_max, rain_rate_min, rain_rate_max, "cool")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("##### Lluvia diaria")
        box_rain = _box_data(daily_rain, color_prec, unit = "mm")

    with col2:
        st.markdown("##### Lluvia últimos 15 min.")
        color = _get_cmap(rain_15min, 0.0, 60.0, "cool")
        box_rain_15min = _box_data(rain_15min, color, unit = "mm")

    with col3:
        st.markdown("##### Intensidad máxima")
        box_rain_rr = _box_data(rain_rate_max, color_rain_rate, unit = "mm/h")

    with col4:
        st.markdown("##### Intensidad")
        box_rain_rr = _box_data(rain_rate_last, color_rain_rate, unit = "mm/h")

    col5, col6, col7 = st.columns(3)

    with col5:
        st.markdown("##### Lluvia última hora")
        color = _get_cmap(rain_60min, 0.0, 180.0, "cool")
        box_rain_1h = _box_data(rain_60min, color, unit = "mm")

    with col6:
        st.markdown("##### Lluvia este mes")
        color = _get_cmap(rain_month, 0.0, 250.0, "cool")
        box_rain_month = _box_data(rain_month, color, unit = "mm")

    with col7:
        st.markdown("##### Lluvia este año")
        color = _get_cmap(rain_month, 0.0, 600.0, "cool")
        box_rain_year = _box_data(rain_year, color, unit = "mm")


def pressure_conditions(data_current):
    st.markdown('## Presión atmosférica actual')
    current_datetime = data_current["ts"].dt.strftime("%d-%m-%Y %H:%M").values.flatten()[0]
    st.text(f"Última actualización: {current_datetime} UTC")

    # datos de la estación meteorológica
    pressure = data_current["bar_sea_level"].values.flatten()[0]
    pressure_abs = data_current["bar_absolute"].values.flatten()[0]
    pressure_trend = data_current["bar_trend"].values.flatten()[0]

    # Obtener colores según la paleta continua
    color_pres = _get_cmap(pressure, pres_min, pres_max, "PuRd")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### Presión barométrica")
        box_pres = _box_data(pressure, color_pres, unit = "hPa")

    with col2:
        st.markdown("##### Presión absoluta")
        color = _get_cmap(pressure_abs, 970.0, 1040.0)
        box_pres_abs = _box_data(pressure_abs, color, unit = "hPa")

    with col3:
        st.markdown("##### Tendencia barométrica")
        box_pres_tr = _box_data(pressure_trend, color = None, unit = "hPa")


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
    color_wind = _get_cmap(wind_speed, wind_min, wind_max, "gist_ncar")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Velocidad viento actual")
        box_wind = _box_data(wind_speed, color_wind, unit = "km/h")

    with col2:
        st.markdown("##### Dirección viento actual")
        box_wind_dir = _box_data(wind_dir, color = None, unit = "°", box_arrow=True)
    
    col3, col4, col5, col6 = st.columns(4)

    with col3:
        st.markdown("##### Velocidad media últimos 2 min.")
        color = _get_cmap(wind_speed_avg_2min, 0.0, 60.0, "gist_ncar")
        box_wind = _box_data(wind_speed_avg_2min, color, unit = "km/h")

    with col4:
        st.markdown("##### Racha últimos 2 min.")
        box_wind = _box_data(wind_gust_2min, color_wind, unit = "km/h")

    with col5:
        st.markdown("##### Dirección media últimos 2 min.")
        box_wind_dir = _box_data(wind_dir_avg_2min, color = None, unit = "°", box_arrow=True)

    with col6:
        st.markdown("##### Dirección racha últimos 2 min.")
        box_wind_dir = _box_data(wind_dir_gust_2min, color = None, unit = "°", box_arrow=True)

    col7, col8, col9, col10 = st.columns(4)

    with col7:
        st.markdown("##### Velocidad media últimos 10 min.")
        color = _get_cmap(wind_speed_avg_2min, 0.0, 50.0, "gist_ncar")
        box_wind = _box_data(wind_speed_avg_10min, color, unit = "km/h")

    with col8:
        st.markdown("##### Racha últimos 10 min.")
        box_wind = _box_data(wind_gust_10min, color_wind, unit = "km/h")

    with col9:
        st.markdown("##### Dirección media últimos 10 min.")
        box_wind_dir = _box_data(wind_dir_avg_10min, color = None, unit = "°", box_arrow=True)

    with col10:
        st.markdown("##### Dirección racha últimos 10 min.")
        box_wind_dir = _box_data(wind_dir_gust_10min, color = None, unit = "°", box_arrow=True)


# ---------------------------------------MAIN PROGRAM------------------------------------------        

while True:
    data_current = download_current_data(station_name = "Sencelles (Ca'n Ignasi)")
    placeholder = st.empty()
    
    with placeholder.container():

        current_conditions(data_current)
        pressure_conditions(data_current)
        temperature_conditions(data_current)
        rain_conditions(data_current)
        wind_conditions(data_current)

        st.write(f"Página actualizada a {pd.to_datetime("now").strftime("%d-%m-%Y %H:%M")}")
    
    time.sleep(60)
    placeholder.empty()    
