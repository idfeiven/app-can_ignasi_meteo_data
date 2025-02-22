import os
import sys
import pandas as pd
import streamlit as st
from datetime import date
import plotly.express as px

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from download_pws_data_weatherlink import download_data


st.title("Gráficas")

# Selector de fecha
datetime = st.date_input("Selecciona una fecha:", value=date.today())
datetime_tomorrow = pd.to_datetime(datetime) + pd.Timedelta("1 day")

todays_data = download_data(station_name = "Sencelles (Ca'n Ignasi)",
                     start_datetime = pd.to_datetime(datetime).strftime("%Y-%m-%d"),
                     end_datetime = pd.to_datetime(datetime_tomorrow).strftime("%Y-%m-%d"),
                     historic = True)

# Selector de variable a graficar
variable = st.selectbox(
    "Selecciona una variable para representar:", 
    options=[col for col in todays_data.columns if "at" not in col and col != "ts"],  # Excluir la columna de tiempo
)

# Crear un gráfico interactivo con Plotly
fig = px.line(
    todays_data,
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

st.plotly_chart(fig)  # Mostrar la gráfica en Streamlit