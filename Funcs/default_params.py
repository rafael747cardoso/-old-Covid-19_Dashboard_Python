
import numpy as np
import pandas as pd
import COVID19Py

path_figs = "Figs/"
data_source = "https://cvtapi.nl"
cases_color = "#169db2"
deaths_color = "#d53343"
recovered_color = "#27a243"
spinner_type = "graph"
cards_colors = {"cases": "info",
                "deaths": "danger",
                "recovered": "success"}
period_options = [{"label": "1 day", "value": 1},
                  {"label": "3 days", "value": 3},
                  {"label": "7 days", "value": 7},
                  {"label": "14 days", "value": 14}]

# Coronavirus data from Johns Hopkins University:
covid19data = COVID19Py.COVID19(url = data_source,
                                data_source = "jhu")

# List of countries:
df_contries = pd.DataFrame(covid19data.getLocations())[["country", "country_code"]].drop_duplicates()
df_contries.reset_index()
countries_options = []
for i in range(0, df_contries.shape[0]):
    countries_options += [{"label": df_contries["country"].iloc[i],
                           "value": df_contries["country_code"].iloc[i]}]


