import os
import sys
import streamlit as st
sys.path.append(os.path.join(os.path.dirname(__file__), "modules"))


homepage = st.Page("modules/homepage.py", title = "Inicio")
current_conditions_page = st.Page("modules/current_conditions_page.py", title = "Condiciones actuales")
daily_summary_page = st.Page("modules/daily_summary_page.py", title = "Resumen diario")
# recent_data_page = st.Page("modules/recent_data_page.py", title = "Recent data")
# historical_data_page = st.Page("modules/historical_data_page.py", title = "Historical data")
# annual_comparison_page = st.Page("modules/annual_comparison_page.py", title = "Annual comparison page")
# statistics_page = st.Page("modules/statistics_page.py", title = "Statistics")
# extreme_data_page = st.Page("modules/extreme_data_page.py", title = "Data extremes")
# indicators_page = st.Page("modules/indicators_page.py", title = "Indicators")
# for multiple pages in one category, define a dictionary

pg = st.navigation([homepage,
                    current_conditions_page,
                    daily_summary_page
                    ]
                  )

pg.run()
