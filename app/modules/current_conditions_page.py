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

def get_cmap(valor, min_val, max_val, cmap_name="coolwarm"):
    norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
    cmap = matplotlib.colormaps.get_cmap(cmap_name)
    color_rgb = cmap(norm(valor))[:3]  # Obtiene el color en formato RGB
    color_hex = mcolors.rgb2hex(color_rgb)  # Convierte a HEX
    return color_hex  # Lo convertimos a formato HEX


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
    color_temp = get_cmap(temperature, temp_min, temp_max, "jet")
    color_hum = get_cmap(humidity, hum_min, hum_max, "BuPu")
    color_wind = get_cmap(wind_speed, wind_min, wind_max, "Greys")
    color_pres = get_cmap(pressure, pres_min, pres_max, "PuRd")
    color_prec = get_cmap(prec_daily, prec_min, prec_max, "Blues")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### Temperatura")
        st.markdown(f"<div style='background-color:{color_temp};padding:10px;border-radius:10px;'><h2>{temperature} °C</h2></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("##### Humedad")
        st.markdown(f"<div style='background-color:{color_hum};padding:10px;border-radius:10px;'><h2>{humidity} %</h2></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("##### Lluvia diaria")
        st.markdown(f"<div style='background-color:{color_prec};padding:10px;border-radius:10px;'><h2>{prec_daily} mm</h2></div>", unsafe_allow_html=True)

    col4, col5, col6 = st.columns(3)
    with col4:
        st.markdown("##### Velocidad del viento")
        st.markdown(f"<div style='background-color:{color_wind};padding:10px;border-radius:10px;'><h2>{wind_speed} km/h</h2></div>", unsafe_allow_html=True)

    with col5:
        st.markdown("##### Dirección del viento")
        st.markdown(f"""
                    <div class="data-box">
                        <h2 class="wind-arrow">&#8593 <!-- Flecha que rota -->
                        ({wind_dir}°)</h2>
                    </div>
                    """, unsafe_allow_html=True)

    with col6:
        st.markdown("##### Presión al nivel del mar")
        st.markdown(f"<div style='background-color:{color_pres};padding:10px;border-radius:10px;'><h2>{pressure} hPa</h2></div>", unsafe_allow_html=True)


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
    color_temp = get_cmap(temperature, temp_min, temp_max, "jet")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("##### Temperatura")
        st.markdown(f"<div style='background-color:{color_temp};padding:10px;border-radius:10px;'><h2>{temperature} °C</h2></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("##### Punto de rocío")
        st.markdown(f"<div style='background-color:{color_temp};padding:10px;border-radius:10px;'><h2>{dewpoint} °C</h2></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("##### Sensación calor")
        st.markdown(f"<div style='background-color:{color_temp};padding:10px;border-radius:10px;'><h2>{heat_index} °C</h2></div>", unsafe_allow_html=True)

    with col4:
        st.markdown("##### Sensación frío")
        st.markdown(f"<div style='background-color:{color_temp};padding:10px;border-radius:10px;'><h2>{wind_chill} °C</h2></div>", unsafe_allow_html=True)


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
    color_prec = get_cmap(daily_rain, prec_min, prec_max, "Blues")
    color_rain_rate = get_cmap(rain_rate_max, rain_rate_min, rain_rate_max, "Blues")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown("##### Lluvia diaria")
        st.markdown(f"<div style='background-color:{color_prec};padding:10px;border-radius:10px;'><h2>{daily_rain} mm</h2></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("##### Lluvia últimos 15 min.")
        st.markdown(f"<div style='background-color:{color_prec};padding:10px;border-radius:10px;'><h2>{rain_15min} mm</h2></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("##### Intensidad máxima")
        st.markdown(f"<div style='background-color:{color_rain_rate};padding:10px;border-radius:10px;'><h2>{rain_rate_max} mm/h</h2></div>", unsafe_allow_html=True)

    with col4:
        st.markdown("##### Intensidad")
        st.markdown(f"<div style='background-color:{color_rain_rate};padding:10px;border-radius:10px;'><h2>{rain_rate_last} mm/h</h2></div>", unsafe_allow_html=True)

    col5, col6, col7 = st.columns(3)

    with col5:
        st.markdown("##### Lluvia última hora")
        st.markdown(f"<div style='background-color:{color_prec};padding:10px;border-radius:10px;'><h2>{rain_60min} mm</h2></div>", unsafe_allow_html=True)

    with col6:
        st.markdown("##### Lluvia este mes")
        st.markdown(f"<div style='background-color:{color_prec};padding:10px;border-radius:10px;'><h2>{rain_month} mm</h2></div>", unsafe_allow_html=True)

    with col7:
        st.markdown("##### Lluvia este año")
        st.markdown(f"<div style='background-color:{color_prec};padding:10px;border-radius:10px;'><h2>{rain_year} mm</h2></div>", unsafe_allow_html=True)


def pressure_conditions(data_current):
    st.markdown('## Presión atmosférica actual')
    current_datetime = data_current["ts"].dt.strftime("%d-%m-%Y %H:%M").values.flatten()[0]
    st.text(f"Última actualización: {current_datetime} UTC")

    # datos de la estación meteorológica
    pressure = data_current["bar_sea_level"].values.flatten()[0]
    pressure_abs = data_current["bar_absolute"].values.flatten()[0]
    pressure_trend = data_current["bar_trend"].values.flatten()[0]

    # Obtener colores según la paleta continua
    color_pres = get_cmap(pressure, pres_min, pres_max, "PuRd")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("##### Presión barométrica")
        st.markdown(f"<div style='background-color:{color_pres};padding:10px;border-radius:10px;'><h2>{pressure} hPa</h2></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("##### Presión absoluta")
        st.markdown(f"<div style='background-color:{color_pres};padding:10px;border-radius:10px;'><h2>{pressure_abs} hPa</h2></div>", unsafe_allow_html=True)

    with col3:
        st.markdown("##### Tendencia barométrica")
        st.markdown(f"<div style=padding:10px;border-radius:10px;'><h2>{pressure_trend} hPa</h2></div>", unsafe_allow_html=True)


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
    color_wind = get_cmap(wind_speed, wind_min, wind_max, "Greys")

    # Mostrar los datos en cuadros grandes con colores de fondo
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("##### Velocidad viento actual")
        st.markdown(f"<div style='background-color:{color_wind};padding:10px;border-radius:10px;'><h2>{wind_speed} km/h</h2></div>", unsafe_allow_html=True)

    with col2:
        st.markdown("##### Dirección viento actual")
        st.markdown(f"""
                    <div class="data-box">
                        <h2 class="wind-arrow">&#8593 <!-- Flecha que rota -->
                        ({wind_dir}°)</h2>
                    </div>
                    """, unsafe_allow_html=True)
    
    col3, col4, col5, col6 = st.columns(4)

    with col3:
        st.markdown("##### Velocidad media últimos 2 min.")
        st.markdown(f"<div style='background-color:{color_wind};padding:10px;border-radius:10px;'><h2>{wind_speed_avg_2min} km/h</h2></div>", unsafe_allow_html=True)

    with col4:
        st.markdown("##### Racha últimos 2 min.")
        st.markdown(f"<div style='background-color:{color_wind};padding:10px;border-radius:10px;'><h2>{wind_gust_2min} km/h</h2></div>", unsafe_allow_html=True)

    with col5:
        st.markdown("##### Dirección media últimos 2 min.")
        st.markdown(f"""
                    <div class="data-box">
                        <h2 class="wind-arrow">&#8593 <!-- Flecha que rota -->
                        ({wind_dir_avg_2min}°)</h2>
                    </div>
                    """, unsafe_allow_html=True)

    with col6:
        st.markdown("##### Dirección racha últimos 2 min.")
        st.markdown(f"""
                    <div class="data-box">
                        <h2 class="wind-arrow">&#8593 <!-- Flecha que rota -->
                        ({wind_dir_gust_2min}°)</h2>
                    </div>
                    """, unsafe_allow_html=True)

    col7, col8, col9, col10 = st.columns(4)

    with col7:
        st.markdown("##### Velocidad media últimos 10 min.")
        st.markdown(f"<div style='background-color:{color_wind};padding:10px;border-radius:10px;'><h2>{wind_speed_avg_10min} km/h</h2></div>", unsafe_allow_html=True)

    with col8:
        st.markdown("##### Racha últimos 10 min.")
        st.markdown(f"<div style='background-color:{color_wind};padding:10px;border-radius:10px;'><h2>{wind_gust_10min} km/h</h2></div>", unsafe_allow_html=True)

    with col9:
        st.markdown("##### Dirección media últimos 10 min.")
        st.markdown(f"""
                    <div class="data-box">
                        <h2 class="wind-arrow">&#8593 <!-- Flecha que rota -->
                        ({wind_dir_avg_10min}°)</h2>
                    </div>
                    """, unsafe_allow_html=True)

    with col10:
        st.markdown("##### Dirección racha últimos 10 min.")
        st.markdown(f"""
                    <div class="data-box">
                        <h2 class="wind-arrow">&#8593 <!-- Flecha que rota -->
                        ({wind_dir_gust_10min}°)</h2>
                    </div>
                    """, unsafe_allow_html=True)
        

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
