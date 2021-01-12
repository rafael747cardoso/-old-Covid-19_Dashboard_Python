
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import COVID19Py
import plotly.express as px
import plotly.graph_objects as go
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from Funcs.default_params import path_figs, data_source, cases_color, deaths_color,\
                                 recovered_color, spinner_type, df_contries, \
                                 countries_options, covid19data
from Funcs.prepare_dataset import prepare_dataset
from Funcs.ui_ts_plot import ui_ts_plot
from Funcs.plot_ts import plot_ts
from Funcs.ui_card_totals import ui_card_totals
from Funcs.ui_trajectories import ui_trajectories
from Funcs.plot_trajectories import plot_trajectories
from Funcs.ui_maps import ui_maps
from Funcs.plot_map import plot_map

#-----------------------------------------------------------------------------------------------------------------------
### Data

# Time Series of the World:
df_ts_world = prepare_dataset(covid19data = covid19data,
                              dataset_type = "time_series_world",
                              chosen_country = "")

df_world_total = prepare_dataset(covid19data = covid19data,
                                 dataset_type = "latest_data_world",
                                 chosen_country = "")

df_all_countries = prepare_dataset(covid19data = covid19data,
                                   dataset_type = "latest_data_all_countries",
                                   chosen_country = "")

#-----------------------------------------------------------------------------------------------------------------------
### One-time calls

def world_total_cases():
    return(format(df_world_total["cases_cumulative"][0], ",").replace(",", " "))

def world_total_deaths():
    return(format(df_world_total["deaths_cumulative"][0], ",").replace(",", " "))

def world_total_recovered():
    return(format(df_world_total["recovered_cumulative"][0], ",").replace(",", " "))


#-----------------------------------------------------------------------------------------------------------------------
### Initialize the dashboard

app = dash.Dash(name = __name__,
                external_stylesheets = ["assets/bootstrap.css"])
server = app.server

#-----------------------------------------------------------------------------------------------------------------------
### Layout

##################################################### World ############################################################

tab_world = html.Div([
    html.Br(),
    html.H3("Time Series for the World",
            style = {"text-align": "center"}),
    html.Br(),
    dcc.Loading(
        id = "loading_world_totals",
        type = spinner_type,
        children = [
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    ui_card_totals(title = "Total Cases",
                                                   content = html.H3(world_total_cases())),
                                    width = 4
                                ),
                                dbc.Col(
                                    ui_card_totals(title = "Total Deaths",
                                                   content = html.H3(world_total_deaths())),
                                    width = 4
                                ),
                                dbc.Col(
                                    ui_card_totals(title = "Total Recovered",
                                                   content = html.H3(world_total_recovered())),
                                    width = 4
                                )
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                html.H5("Updated in " + df_ts_world["date"].values[-1].astype("str")[0:10])
                            ]
                        ),
                        dbc.Row(
                            [
                                html.H5("Data source:  " + data_source)
                            ]
                        )
        
                    ]
                ),
                className = "card_totals",
                color = "primary"
            )
        ]
    ),
    html.Br(),
    dcc.Loading(
        id = "loading_world_cum",
        type = spinner_type,
        children = [
            dbc.Card(
                [
                    dbc.CardHeader("Cumulative"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "world_ts_cases_cum"),
                                        width = 4),
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "world_ts_deaths_cum"),
                                        width = 4),
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "world_ts_recovered_cum"),
                                        width = 4)
                                ]
                            )
                        ]
                    )
                ],
                className = "card_header_color_cum",
                color = "primary",
                outline = True,
                inverse = True
            )
        ]
    ),
    html.Br(),
    dcc.Loading(
        id = "loading_world_daily",
        type = spinner_type,
        children = [
            dbc.Card(
                [
                    dbc.CardHeader("Daily"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "world_ts_cases_daily"),
                                        width = 4),
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "world_ts_deaths_daily"),
                                        width = 4),
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "world_ts_recovered_daily"),
                                        width = 4)
                                ]
                            )
                        ]
                    )
                ],
                className = "card_header_color_daily",
                color = "warning",
                outline = True,
                inverse = True
            )
        ]
    ),
    html.Br()
])

#################################################### Country ###########################################################

tab_country = html.Div([
    html.Br(),
    html.H3(id = "chosen_country_name",
            children = [],
            style = {"text-align": "center"}),
    html.Br(),
    html.H4("Select a country:",
            style = {"margin-left": "1.5rem"}),
    html.Br(),
    dcc.Dropdown(id = "chosen_country",
                 className = "dash-bootstrap",
                 options = countries_options,
                 value = countries_options[0]["value"],
                 style = {"width": "50%",
                          "margin-left": "1.3rem"}),
    html.Br(),
    dcc.Loading(
        id = "loading_country_totals",
        type = spinner_type,
        children = [
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    ui_card_totals(title = "Total Cases",
                                                   content = html.H3(id = "country_total_cases",
                                                                     children = [])),
                                    width = 4
                                ),
                                dbc.Col(
                                    ui_card_totals(title = "Total Deaths",
                                                   content = html.H3(id = "country_total_deaths",
                                                                     children = [])),
                                    width = 4
                                ),
                                dbc.Col(
                                    ui_card_totals(title = "Total Recovered",
                                                   content = html.H3(id = "country_total_recovered",
                                                                     children = [])),
                                    width = 4
                                )
                            ]
                        ),
                        html.Br(),
                        dbc.Row(
                            [
                                html.H5("Updated in " + df_ts_world["date"].values[-1].astype("str")[0:10])
                            ]
                        ),
                        dbc.Row(
                            [
                                html.H5("Data source:  " + data_source)
                            ]
                        )
        
                    ]
                ),
                className = "card_totals",
                color = "primary"
            )
        ]
    ),
    html.Br(),
    dcc.Loading(
        id = "loading_country_cum",
        type = spinner_type,
        children = [
            dbc.Card(
                [
                    dbc.CardHeader("Cumulative"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "country_ts_cases_cum"),
                                        width = 4),
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "country_ts_deaths_cum"),
                                        width = 4),
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "country_ts_recovered_cum"),
                                        width = 4)
                                ]
                            )
                        ]
                    )
                ],
                className = "card_header_color_cum",
                color = "primary",
                outline = True,
                inverse = True
            )
        ]
    ),
    html.Br(),
    dcc.Loading(
        id = "loading_country_daily",
        type = spinner_type,
        children = [
            dbc.Card(
                [
                    dbc.CardHeader("Daily"),
                    dbc.CardBody(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "country_ts_cases_daily"),
                                        width = 4),
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "country_ts_deaths_daily"),
                                        width = 4),
                                    dbc.Col(
                                        ui_ts_plot(plot_ids = "country_ts_recovered_daily"),
                                        width = 4)
                                ]
                            )
                        ]
                    )
                ],
                className = "card_header_color_daily",
                color = "warning",
                outline = True,
                inverse = True
            )
        ]
    ),
    html.Br()
])

############################################### Comparision ############################################################

tab_comparison = html.Div([
    html.Br(),
    html.H3("Countries trajectories",
            style = {"text-align": "center"}),
    html.Br(),
    ui_trajectories(type = "cases"),
    html.Br(),
    ui_trajectories(type = "deaths"),
    html.Br(),
    ui_trajectories(type = "recovered"),
    html.Br()
])

################################################# Maps #################################################################

tab_maps = html.Div([
    html.Br(),
    html.H3("Maps",
            style = {"text-align": "center"}),
    html.Br(),
    ui_maps(),
    html.Br()
])


# Layout:
app.layout = html.Div(
    [
        html.Div(
            [
                html.Br(),
                html.H2("Covid-19 Dashboard",
                        style = {"text-align": "center"}),
                html.Br(),
                dbc.Tabs(
                    [
                        dbc.Tab(children = tab_world,
                                label = "World Panel"),
                        dbc.Tab(children = tab_country,
                                label = "Country Panel"),
                        dbc.Tab(children = tab_comparison,
                                label = "Countries Comparison"),
                        dbc.Tab(children = tab_maps,
                                label = "Maps")
                    ]                    
                )
            ]
        )
    ]
)

#-----------------------------------------------------------------------------------------------------------------------
### Callbacks

################################################## World ###############################################################

# Plot Time Series Cases Cumulative:
@app.callback(
    Output(component_id = "plot_world_ts_cases_cum", component_property = "figure"),
    [Input(component_id = "scale_world_ts_cases_cum", component_property = "value")]
)
def update_plot_world_ts_cases_cum(scale_world_ts_cases_cum):    
    plot_world_ts_cases_cum = plot_ts(df = df_ts_world,
                                      y_var = "cases_cum",
                                      y_scale = scale_world_ts_cases_cum,
                                      type_color = cases_color)
    return(plot_world_ts_cases_cum)

# Plot Time Series Deaths Cumulative:
@app.callback(
    Output(component_id = "plot_world_ts_deaths_cum", component_property = "figure"),
    [Input(component_id = "scale_world_ts_deaths_cum", component_property = "value")]
)
def update_plot_world_ts_deaths_cum(scale_world_ts_deaths_cum):
    plot_world_ts_deaths_cum = plot_ts(df = df_ts_world,
                                       y_var = "deaths_cum",
                                       y_scale = scale_world_ts_deaths_cum,
                                       type_color = deaths_color)
    return(plot_world_ts_deaths_cum)

# Plot Time Series Recovered Cumulative:
@app.callback(
    Output(component_id = "plot_world_ts_recovered_cum", component_property = "figure"),
    [Input(component_id = "scale_world_ts_recovered_cum", component_property = "value")]
)
def update_plot_world_ts_recovered_cum(scale_world_ts_recovered_cum):
    plot_world_ts_recovered_cum = plot_ts(df = df_ts_world,
                                          y_var = "recovered_cum",
                                          y_scale = scale_world_ts_recovered_cum,
                                          type_color = recovered_color)
    return(plot_world_ts_recovered_cum)

# Plot Time Series Cases Daily:
@app.callback(
    Output(component_id = "plot_world_ts_cases_daily", component_property = "figure"),
    [Input(component_id = "scale_world_ts_cases_daily", component_property = "value")]
)
def update_plot_world_ts_cases_daily(scale_world_ts_cases_daily):    
    plot_world_ts_cases_daily = plot_ts(df = df_ts_world,
                                        y_var = "cases_daily",
                                        y_scale = scale_world_ts_cases_daily,
                                        type_color = cases_color)
    return(plot_world_ts_cases_daily)

# Plot Time Series Deaths Daily:
@app.callback(
    Output(component_id = "plot_world_ts_deaths_daily", component_property = "figure"),
    [Input(component_id = "scale_world_ts_deaths_daily", component_property = "value")]
)
def update_plot_world_ts_deaths_daily(scale_world_ts_deaths_daily):
    plot_world_ts_deaths_daily = plot_ts(df = df_ts_world,
                                         y_var = "deaths_daily",
                                         y_scale = scale_world_ts_deaths_daily,
                                         type_color = deaths_color)
    return(plot_world_ts_deaths_daily)

# Plot Time Series Recovered Daily:
@app.callback(
    Output(component_id = "plot_world_ts_recovered_daily", component_property = "figure"),
    [Input(component_id = "scale_world_ts_recovered_daily", component_property = "value")]
)
def update_plot_world_ts_recovered_daily(scale_world_ts_recovered_daily):
    plot_world_ts_recovered_daily = plot_ts(df = df_ts_world,
                                            y_var = "recovered_daily",
                                            y_scale = scale_world_ts_recovered_daily,
                                            type_color = recovered_color)
    return(plot_world_ts_recovered_daily)

################################################# Country ##############################################################

# Title with the chosen country name:
@app.callback(
    Output(component_id = "chosen_country_name", component_property = "children"),
    [Input(component_id = "chosen_country", component_property = "value")]
)
def update_chosen_country_title(chosen_country):    
    country_name = df_contries["country"].iloc[np.where(df_contries["country_code"] == chosen_country)].values[0]
    country_name = "Time Series for " + country_name
    return(country_name)

# Total Cases:
@app.callback(
    Output(component_id = "country_total_cases", component_property = "children"),
    [Input(component_id = "chosen_country", component_property = "value")]
)
def update_country_total_cases(chosen_country):
    df = prepare_dataset(covid19data = covid19data,
                         dataset_type = "latest_data_country",
                         chosen_country = chosen_country)
    return(format(df["cases_cumulative"].iloc[0], ",").replace(",", " "))

# Total Deaths:
@app.callback(
    Output(component_id = "country_total_deaths", component_property = "children"),
    [Input(component_id = "chosen_country", component_property = "value")]
)
def update_country_total_deaths(chosen_country):
    df = prepare_dataset(covid19data = covid19data,
                         dataset_type = "latest_data_country",
                         chosen_country = chosen_country)
    return(format(df["deaths_cumulative"].iloc[0], ",").replace(",", " "))

# Total Recovered:
@app.callback(
    Output(component_id = "country_total_recovered", component_property = "children"),
    [Input(component_id = "chosen_country", component_property = "value")]
)
def update_country_total_recovered(chosen_country):
    df = prepare_dataset(covid19data = covid19data,
                         dataset_type = "latest_data_country",
                         chosen_country = chosen_country)
    return(format(df["recovered_cumulative"].iloc[0], ",").replace(",", " "))

# Plot Time Series Cases Cumulative:
@app.callback(
    Output(component_id = "plot_country_ts_cases_cum", component_property = "figure"),
    [Input(component_id = "chosen_country", component_property = "value"),
     Input(component_id = "scale_country_ts_cases_cum", component_property = "value")]
)
def update_plot_country_ts_cases_cum(chosen_country,
                                     scale_country_ts_cases_cum):
    df_ts_country = prepare_dataset(covid19data = covid19data,
                                    dataset_type = "time_series_country",
                                    chosen_country = chosen_country)    
    plot_country_ts_cases_cum = plot_ts(df = df_ts_country,
                                        y_var = "cases_cum",
                                        y_scale = scale_country_ts_cases_cum,
                                        type_color = cases_color)
    return(plot_country_ts_cases_cum)

# Plot Time Series Deaths Cumulative:
@app.callback(
    Output(component_id = "plot_country_ts_deaths_cum", component_property = "figure"),
    [Input(component_id = "chosen_country", component_property = "value"),
     Input(component_id = "scale_country_ts_deaths_cum", component_property = "value")]
)
def update_plot_country_ts_deaths_cum(chosen_country,
                                      scale_country_ts_deaths_cum):
    df_ts_country = prepare_dataset(covid19data = covid19data,
                                    dataset_type = "time_series_country",
                                    chosen_country = chosen_country)    
    plot_country_ts_deaths_cum = plot_ts(df = df_ts_country,
                                        y_var = "deaths_cum",
                                        y_scale = scale_country_ts_deaths_cum,
                                        type_color = deaths_color)
    return(plot_country_ts_deaths_cum)

# Plot Time Series Recovered Cumulative:
@app.callback(
    Output(component_id = "plot_country_ts_recovered_cum", component_property = "figure"),
    [Input(component_id = "chosen_country", component_property = "value"),
     Input(component_id = "scale_country_ts_recovered_cum", component_property = "value")]
)
def update_plot_country_ts_recovered_cum(chosen_country,
                                         scale_country_ts_recovered_cum):
    df_ts_country = prepare_dataset(covid19data = covid19data,
                                    dataset_type = "time_series_country",
                                    chosen_country = chosen_country)    
    plot_country_ts_recovered_cum = plot_ts(df = df_ts_country,
                                        y_var = "recovered_cum",
                                        y_scale = scale_country_ts_recovered_cum,
                                        type_color = recovered_color)
    return(plot_country_ts_recovered_cum)

# Plot Time Series Cases Daily:
@app.callback(
    Output(component_id = "plot_country_ts_cases_daily", component_property = "figure"),
    [Input(component_id = "chosen_country", component_property = "value"),
     Input(component_id = "scale_country_ts_cases_daily", component_property = "value")]
)
def update_plot_country_ts_cases_daily(chosen_country,
                                       scale_country_ts_cases_daily):
    df_ts_country = prepare_dataset(covid19data = covid19data,
                                    dataset_type = "time_series_country",
                                    chosen_country = chosen_country)    
    plot_country_ts_cases_daily = plot_ts(df = df_ts_country,
                                          y_var = "cases_daily",
                                          y_scale = scale_country_ts_cases_daily,
                                          type_color = cases_color)
    return(plot_country_ts_cases_daily)

# Plot Time Series Deaths Daily:
@app.callback(
    Output(component_id = "plot_country_ts_deaths_daily", component_property = "figure"),
    [Input(component_id = "chosen_country", component_property = "value"),
     Input(component_id = "scale_country_ts_deaths_daily", component_property = "value")]
)
def update_plot_country_ts_deaths_daily(chosen_country,
                                        scale_country_ts_deaths_daily):
    df_ts_country = prepare_dataset(covid19data = covid19data,
                                    dataset_type = "time_series_country",
                                    chosen_country = chosen_country)    
    plot_country_ts_deaths_daily = plot_ts(df = df_ts_country,
                                           y_var = "deaths_daily",
                                           y_scale = scale_country_ts_deaths_daily,
                                           type_color = deaths_color)
    return(plot_country_ts_deaths_daily)

# Plot Time Series Recovered Daily:
@app.callback(
    Output(component_id = "plot_country_ts_recovered_daily", component_property = "figure"),
    [Input(component_id = "chosen_country", component_property = "value"),
     Input(component_id = "scale_country_ts_recovered_daily", component_property = "value")]
)
def update_plot_country_ts_recovered_daily(chosen_country,
                                           scale_country_ts_recovered_daily):
    df_ts_country = prepare_dataset(covid19data = covid19data,
                                    dataset_type = "time_series_country",
                                    chosen_country = chosen_country)    
    plot_country_ts_recovered_daily = plot_ts(df = df_ts_country,
                                              y_var = "recovered_daily",
                                              y_scale = scale_country_ts_recovered_daily,
                                              type_color = recovered_color)
    return(plot_country_ts_recovered_daily)


############################################### Comparision ############################################################

# Plot Trajectories for Cases:
@app.callback(
    Output(component_id = "plot_trajectories_cases", component_property = "figure"),
    [Input(component_id = "chosen_countries_trajectories_cases", component_property = "value"),
     Input(component_id = "chosen_period_trajectories_cases", component_property = "value"),
     Input(component_id = "scale_trajectories_cases", component_property = "value")]
)
def update_plot_trajectories_cases(chosen_countries_trajectories_cases,
                                   chosen_period_trajectories_cases,
                                   scale_trajectories_cases):    
    df = pd.DataFrame({"country_code": [],
                       "country": [],
                       "cases_cum": [],
                       "cases_daily": []})
    for country in chosen_countries_trajectories_cases:
        df_country = prepare_dataset(covid19data = covid19data,
                                     dataset_type = "time_series_country",
                                     chosen_country = country)
        df_country = df_country[["country_code",
                                 "country",
                                 "cases_cum",
                                 "cases_daily"]]
        df = df.append(df_country)
    plot_trajectories_cases = plot_trajectories(df = df,
                                                type_var = "cases",
                                                period = chosen_period_trajectories_cases,
                                                scale = scale_trajectories_cases)
    return(plot_trajectories_cases)

# Plot Trajectories for Deaths:
@app.callback(
    Output(component_id = "plot_trajectories_deaths", component_property = "figure"),
    [Input(component_id = "chosen_countries_trajectories_deaths", component_property = "value"),
     Input(component_id = "chosen_period_trajectories_deaths", component_property = "value"),
     Input(component_id = "scale_trajectories_deaths", component_property = "value")]
)
def update_plot_trajectories_deaths(chosen_countries_trajectories_deaths,
                                   chosen_period_trajectories_deaths,
                                   scale_trajectories_deaths):    
    df = pd.DataFrame({"country_code": [],
                       "country": [],
                       "deaths_cum": [],
                       "deaths_daily": []})
    for country in chosen_countries_trajectories_deaths:
        df_country = prepare_dataset(covid19data = covid19data,
                                     dataset_type = "time_series_country",
                                     chosen_country = country)
        df_country = df_country[["country_code",
                                 "country",
                                 "deaths_cum",
                                 "deaths_daily"]]
        df = df.append(df_country)
    plot_trajectories_deaths = plot_trajectories(df = df,
                                                 type_var = "deaths",
                                                 period = chosen_period_trajectories_deaths,
                                                 scale = scale_trajectories_deaths)    
    return(plot_trajectories_deaths)

# Plot Trajectories for Recovered:
@app.callback(
    Output(component_id = "plot_trajectories_recovered", component_property = "figure"),
    [Input(component_id = "chosen_countries_trajectories_recovered", component_property = "value"),
     Input(component_id = "chosen_period_trajectories_recovered", component_property = "value"),
     Input(component_id = "scale_trajectories_recovered", component_property = "value")]
)
def update_plot_trajectories_recovered(chosen_countries_trajectories_recovered,
                                   chosen_period_trajectories_recovered,
                                   scale_trajectories_recovered):    
    df = pd.DataFrame({"country_code": [],
                       "country": [],
                       "recovered_cum": [],
                       "recovered_daily": []})
    for country in chosen_countries_trajectories_recovered:
        df_country = prepare_dataset(covid19data = covid19data,
                                     dataset_type = "time_series_country",
                                     chosen_country = country)
        df_country = df_country[["country_code",
                                 "country",
                                 "recovered_cum",
                                 "recovered_daily"]]
        df = df.append(df_country)
    plot_trajectories_recovered = plot_trajectories(df = df,
                                                    type_var = "recovered",
                                                    period = chosen_period_trajectories_recovered,
                                                    scale = scale_trajectories_recovered)    
    return(plot_trajectories_recovered)


################################################# Maps #################################################################

# Choropleth Map:
@app.callback(
    Output(component_id = "map_choropleth", component_property = "figure"),
    [Input(component_id = "map_var", component_property = "value")]
)
def update_map(map_var):
    map_world = plot_map(df = df_all_countries,
                         var = map_var)
    return(map_world)


#-----------------------------------------------------------------------------------------------------------------------
### Run the dashboard

# app.run_server(debug = True)
if __name__ == "__main__":
    app.run_server(debug = True)


