import matplotlib
import streamlit as st
import plotly.express as px
import matplotlib.colors as mcolors


def parse_cols_historical_data(data):

    data = data.copy()
    data["Precipitación acumulada (mm)"] = data['rainfall_mm'].cumsum()

    data.rename(columns = {'bar_absolute': 'Presión absoluta (hPa)',
                                'bar_sea_level': 'Presión al nivel del mar (hPa)',
                                'bar_lo': 'Presión mínima al nivel del mar (hPa)',
                                'bar_hi': 'Presión máxima al nivel del mar (hPa)',
                                'wind_speed_avg': 'Velocidad del viento media (km/h)',
                                'dew_point_last': 'Punto de rocío (°C)',
                                'temp_hi': 'Temperatura máxima (°C)',
                                'temp_lo': 'Temperatura mínima (°C)',
                                'heat_index_hi': 'Sensación de calor máxima (°C)',
                                'heat_index_last': 'Sensación de calor (°C)',
                                'wind_dir_of_prevail': 'Dirección media del viento (°)',
                                'rainfall_mm': 'Precipitación (mm)',
                                'rain_rate_hi_mm': 'Intensidad máxima de precipitación (mm/h)',
                                'hum_lo': 'Humedad mínima (%)',
                                'hum_hi': 'Humedad máxima (%)',
                                'wind_speed_hi': 'Racha de viento máxima (km/h)',
                                'temp_last': 'Temperatura (°C)',
                                'temp_avg': 'Temperatura media (°C)',
                                'hum_last': 'Humedad (%)',
                                'wind_speed_hi_dir': 'Dirección racha de viento máxima (°)',
                                'dew_point_hi': 'Punto de rocío máximo (°C)',
                                'dew_point_lo': 'Punto de rocío mínimo (°C)'
                                }, inplace = True)
    
    return data


def plot_interactive(data, coord, variable):

    # Crear un gráfico interactivo con Plotly
    fig = px.line(
        data,
        x=coord,  # Asegúrate de que la API devuelve una columna 'hora'
        y=variable,  # Ajusta esto a la variable que quieras visualizar
        title=f"Evolución de {variable}",
        labels={"ts": "Fecha/hora (UTC)", f"{variable}": variable},
        markers=True
    )

    # Aumentar el grosor de la línea
    fig.update_traces(line=dict(width=4))  # Ajustar grosor (por defecto es 2)

    # Añadir Grid (Cuadrícula)
    fig.update_layout(
        xaxis_showgrid=True,   # Activar la cuadrícula en el eje X
        yaxis_showgrid=True,   # Activar la cuadrícula en el eje Y
        xaxis_gridcolor="lightgray",  # Color de la cuadrícula X
        yaxis_gridcolor="lightgray",  # Color de la cuadrícula Y
        xaxis_gridwidth=0.2,   # Grosor de la cuadrícula X
        yaxis_gridwidth=0.2    # Grosor de la cuadrícula Y
    )

    return fig


def get_range_vals_for_color_norm():

    temp_min, temp_max = -10, 45
    hum_min, hum_max = 0, 100
    wind_min, wind_max = 0, 100
    pres_min, pres_max = 980, 1050
    prec_min, prec_max = 0, 200
    rain_rate_min, rain_rate_max = 0, 1440

    range_vals = dict({"temp": [temp_min, temp_max],
          "hum": [hum_min, hum_max],
          "wind": [wind_min, wind_max],
          "pres": [pres_min, pres_max],
          "prec": [prec_min, prec_max],
          "rain_rate": [rain_rate_min, rain_rate_max]})
    
    return range_vals


def get_cmap(valor, min_val, max_val, cmap_name="coolwarm"):
    norm = mcolors.Normalize(vmin=min_val, vmax=max_val)
    cmap = matplotlib.colormaps.get_cmap(cmap_name)
    color_rgb = cmap(norm(valor))[:3]  # Obtiene el color en formato RGB
    color_hex = mcolors.rgb2hex(color_rgb)  # Convierte a HEX
    return color_hex  # Lo convertimos a formato HEX


def box_data(data, color, unit, box_arrow = False):
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
        box = st.markdown(f"<div style=background-color:{color};padding:10px;border-radius:10px;'><h2>{data} {unit}</h2></div>", unsafe_allow_html=True)
    else:
        box = st.markdown(f"<div style=padding:10px;border-radius:10px;'><h2>{data} {unit}</h2></div>", unsafe_allow_html=True)

    return box