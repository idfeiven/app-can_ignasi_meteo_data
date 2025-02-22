import matplotlib
import streamlit as st
import matplotlib.colors as mcolors


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