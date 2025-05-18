import os
import sys
import pandas as pd
import streamlit as st
from datetime import date
from common import parse_cols_historical_data, plot_interactive
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from download_pws_data_weatherlink import download_data


# -----------------------------------MAIN PROGRAM-------------------------------------------

st.set_page_config(
    page_title="Gráficas",
    page_icon=":bar_chart:",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Gráficas")

# Selector de fecha
datetime = st.date_input("Selecciona una fecha:", value=date.today())
datetime_tomorrow = pd.to_datetime(datetime) + pd.Timedelta("1 day")

todays_data = download_data(station_name = "Sencelles (Ca'n Ignasi)",
                     start_datetime = pd.to_datetime(datetime).strftime("%Y-%m-%d"),
                     end_datetime = pd.to_datetime(datetime_tomorrow).strftime("%Y-%m-%d"),
                     historic = True)
todays_data = pd.DataFrame(todays_data)

if not todays_data.empty:
    todays_data = parse_cols_historical_data(todays_data)

    # Selector de variable a graficar
    variable = st.selectbox(
        "Selecciona una variable para representar:", 
        options=[col for col in todays_data.columns if "_at" not in col and col != "ts"],  # Excluir la columna de tiempo
    )

    fig = plot_interactive(todays_data, coord = "ts", variable = variable)

    st.plotly_chart(fig)  # Mostrar la gráfica en Streamlit
else:
    st.write("No existen datos para la fecha seleccionada. Selecciona una fecha superior al 25/02/2022.")