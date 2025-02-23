import os
import sys
import calendar
import matplotlib
import pandas as pd
import streamlit as st
from datetime import date
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from common import parse_cols_historical_data, plot_interactive
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'data')))
from download_pws_data_weatherlink import download_data


# -------------------------------------FUNCTIONS-----------------------------------

def get_current_year_month():
    # Obtener el año y mes actuales
    today = date.today()
    year_actual = today.year
    month_actual = today.month

    return year_actual, month_actual 


def get_months_dict():
    # Selector de mes
    months = {
        1: "Enero", 2: "Febrero", 3: "Marzo", 4: "Abril", 5: "Mayo", 6: "Junio",
        7: "Julio", 8: "Agosto", 9: "Septiembre", 10: "Octubre", 11: "Noviembre", 12: "Diciembre"
    }

    return months 


def get_month_dates(selected_month, selected_year):

    # Obtener número de días del mes seleccionado
    num_days = calendar.monthrange(selected_year, selected_month)[1]

    date_month_min = date(selected_year, selected_month, 1)
    date_month_max = date(selected_year, selected_month, num_days)

    dates = pd.date_range(date_month_min, date_month_max, freq = "D")

    return num_days, date_month_min, date_month_max, dates 


def get_df_data_month(dates, num_days):
    data_month = pd.DataFrame()
    count = 0

    if data_month not in st.session_state:

        with st.spinner(f"🔄Descargando datos..."):

            for datetime in dates:
                count += 1
                start = datetime.strftime("%Y-%m-%d")
                end = datetime + pd.Timedelta("1 day")
                end = end.strftime("%Y-%m-%d")

                data_day = download_data(station_name = "Sencelles (Ca'n Ignasi)",
                                        start_datetime = start,
                                        end_datetime = end,
                                        historic = True)
                
                data_month = pd.concat([data_month, data_day], axis = 0)
                st.session_state.data_month = data_month

        st.success("✅Datos descargados")

    return data_month


def get_value_ranges():

    ranges = {
        "Temperatura máxima (°C)": (-10, 45),
        "Temperatura mínima (°C)": (-10, 45),
        "Temperatura media (°C)": (-10, 45),
        "Velocidad del viento media (km/h)": (0, 60),
        "Dirección media del viento (°)": (0, 360),
        "Racha de viento máxima (km/h)": (0, 100),
        "Humedad (%)": (0, 100),
        "Presión al nivel del mar (hPa)": (980, 1045),
        "Precipitación (mm)": (0, 100),
        "Intensidad máxima de precipitación (mm/h)": (0, 1440)
    }

    return ranges 


def get_cmaps():

    # Definir paletas de colores diferentes para cada columna
    colormap = {
        "Temperatura máxima (°C)": "gist_rainbow_r",   
        "Temperatura mínima (°C)": "gist_rainbow_r",  
        "Temperatura media (°C)": "gist_rainbow_r",  
        "Velocidad del viento media (km/h)": "gist_ncar",
        "Dirección media del viento (°)": "grey",
        "Racha de viento máxima (km/h)": "gist_ncar",  
        "Humedad (%)": "BuPu",   
        "Presión al nivel del mar (hPa)": "PuRd",
        "Precipitación (mm)": "cool",
        "Intensidad máxima de precipitación (mm/h)": "cool",
                }
    
    return colormap 


# Función para mapear valores a colores normalizados
def color_cell(val, col, ranges, colormap):
    vmin, vmax = ranges[col]  # Obtener mínimo y máximo de la columna
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)  # Normalizar
    cmap_name = colormap[col]  # Obtener la paleta de colores
    cmap = matplotlib.colormaps.get_cmap(cmap_name)
    rgba = cmap(norm(val))  # Obtener el color en formato RGBA
    color_hex = mcolors.rgb2hex(rgba[:3])  # Convertir a HEX
    return f"background-color: {color_hex}; color: black;"


# Aplicar colores por columna
def apply_colors(df, ranges, colormap):
    return df.style.apply(lambda col: col.map(lambda val: color_cell(val, col.name, ranges, colormap))).format("{:.1f}")


def get_df_month_summary(data_month):

    data_month.reset_index(inplace = True)
    data_month.drop('index', axis = 1, inplace=True)
    data_month = data_month[[col for col in data_month.columns if "_at" not in col]]
    data_month = parse_cols_historical_data(data_month)

    cols_max = ['Temperatura máxima (°C)', 'Intensidad máxima de precipitación (mm/h)',
                'Racha de viento máxima (km/h)']
    data_month_max = data_month.set_index("ts").resample("D").max()[cols_max]

    cols_min = ['Temperatura mínima (°C)']
    data_month_min = data_month.set_index("ts").resample("D").min()[cols_min]

    cols_mean = ['Presión al nivel del mar (hPa)', 'Velocidad del viento media (km/h)',
                'Temperatura media (°C)', 'Humedad (%)', 'Dirección media del viento (°)']
    data_month_mean = data_month.set_index("ts").resample("D").mean()[cols_mean]

    cols_prec = ['Precipitación (mm)']
    data_month_prec = data_month.set_index("ts").resample("D").sum()[cols_prec]

    df_month_summary = pd.concat([data_month_max,
                                data_month_min,
                                data_month_mean,
                                data_month_prec], axis = 1)
    df_month_summary = df_month_summary.iloc[1:].round(1)

    cols_order = ['Temperatura máxima (°C)', 'Temperatura mínima (°C)', 'Temperatura media (°C)',
                'Velocidad del viento media (km/h)', 'Dirección media del viento (°)',
                'Racha de viento máxima (km/h)', 'Humedad (%)', 'Presión al nivel del mar (hPa)',
                'Precipitación (mm)', 'Intensidad máxima de precipitación (mm/h)']
    df_month_summary = df_month_summary[cols_order]
    df_month_summary.index.rename("Fecha", inplace = True)
    df_month_summary.index = df_month_summary.index.strftime("%Y-%m-%d")

    return df_month_summary


# -------------------------------------MAIN PROGRAM-----------------------------------

year_actual, month_actual= get_current_year_month()
months = get_months_dict()

st.title("Resumen mensual")

# Selector de año (últimos 10 años)
years = list(range(year_actual - 3, year_actual + 1 ))
selected_year = st.selectbox("Selecciona un año:", options=years, index=years.index(year_actual))
selected_month = st.selectbox("Selecciona un mes:", options=list(months.keys()), format_func=lambda x: months[x], index=month_actual - 1)

num_days, date_month_min, date_month_max, dates = get_month_dates(selected_month, selected_year)
data_month = get_df_data_month(dates, num_days)

df_month_summary = get_df_month_summary(data_month)

ranges = get_value_ranges()
colormap = get_cmaps()
st.dataframe(apply_colors(df_month_summary, ranges, colormap))


st.markdown("## Gráficas")

if df_month_summary not in st.session_state:
   st.session_state.df_month_summary = df_month_summary

df_month_summary = st.session_state.df_month_summary

# Selector de variable a graficar
variable = st.selectbox(
    "Selecciona una variable para representar:", 
    options=df_month_summary.columns,  # Excluir la columna de tiempo
)
fig = plot_interactive(df_month_summary, coord = df_month_summary.index, variable = variable)
st.plotly_chart(fig)
