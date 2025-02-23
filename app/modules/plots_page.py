import os
import sys
import pandas as pd
import streamlit as st
from datetime import date
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from download_pws_data_weatherlink import download_data


# -----------------------------------FUNCTIONS-------------------------------------------

def parse_cols(data):

    data["Precipitación acumulada (mm)"] = data['rainfall_mm'].cumsum()

    data.rename(columns = {'bar_absolute': 'Presión absoluta (hPa)',
                                'bar_sea_level': 'Presión al nivel del mar (hPa)',
                                'bar_lo': 'Presión mínima al nivel del mar (hPa)',
                                'bar_hi': 'Presión máxima al nivel del mar (hPa)',
                                'wind_speed_avg': 'Velocidad del viento media (km/h)',
                                'wind_chill_last': 'Sensación de frío (°C)',
                                'solar_rad_hi': 'Radiación solar máxima (W/m2)',
                                'dew_point_last': 'Punto de rocío (°C)',
                                'temp_hi': 'Temperatura máxima (°C)',
                                'temp_lo': 'Temperatura mínima (°C)',
                                'wind_dir_of_prevail': 'Dirección media del viento (°)',
                                'rainfall_mm': 'Precipitación (mm)',
                                'hum_lo': 'Humedad mínima (%)',
                                'hum_hi': 'Humedad máxima (%)',
                                'wind_speed_hi': 'Racha de viento máxima (km/h)',
                                'temp_last': 'Temperatura (°C)',
                                'temp_avg': 'Temperatura media (°C)',
                                'hum_last': 'Humedad (%)',
                                'wind_chill_lo': 'Sensación de frío mínima (°C)',
                                'wind_speed_hi_dir': 'Dirección racha de viento máxima (°)',
                                'dew_point_hi': 'Punto de rocío máximo (°C)',
                                'dew_point_lo': 'Punto de rocío mínimo (°C)'
                                }, inplace = True)
    
    return data


def plot_interactive(data, variable):

    # Crear un gráfico interactivo con Plotly
    fig = px.line(
        data,
        x="ts",  # Asegúrate de que la API devuelve una columna 'hora'
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

# -----------------------------------MAIN PROGRAM-------------------------------------------

st.title("Gráficas")

# Selector de fecha
datetime = st.date_input("Selecciona una fecha:", value=date.today())
datetime_tomorrow = pd.to_datetime(datetime) + pd.Timedelta("1 day")

todays_data = download_data(station_name = "Sencelles (Ca'n Ignasi)",
                     start_datetime = pd.to_datetime(datetime).strftime("%Y-%m-%d"),
                     end_datetime = pd.to_datetime(datetime_tomorrow).strftime("%Y-%m-%d"),
                     historic = True)
todays_data = parse_cols(todays_data)

# Selector de variable a graficar
variable = st.selectbox(
    "Selecciona una variable para representar:", 
    options=[col for col in todays_data.columns if "at" not in col and col != "ts"],  # Excluir la columna de tiempo
)

fig = plot_interactive(todays_data, variable)

st.plotly_chart(fig)  # Mostrar la gráfica en Streamlit