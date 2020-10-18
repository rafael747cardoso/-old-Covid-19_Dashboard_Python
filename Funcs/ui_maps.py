
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Funcs.default_params import spinner_type, cards_colors

def ui_maps():
    
    """
    UI for the choropleth maps.
    """
    
    ui_block = dcc.Loading(
        id = "loading_map",
        type = spinner_type,
        children = 
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Graph(id = "map_choropleth",
                                  figure = {}),
                        width = 9
                    ),
                    dbc.Col(
                        dbc.RadioItems(
                            id = "map_var",
                            options = 
                            [
                                {"label": "Daily Cases", "value": "cases_daily"},
                                {"label": "Daily Deaths", "value": "deaths_daily"},
                                {"label": "Daily Recovered", "value": "recovered_daily"},
                                {"label": "Cumulative Cases", "value": "cases_cumulative"},
                                {"label": "Cumulative Deaths", "value": "deaths_cumulative"},
                                {"label": "Cumulative Recovered", "value": "recovered_cumulative"},
                                {"label": "Daily Cases per 1e6 Population", "value": "cases_daily_1e6_pop"},
                                {"label": "Daily Deaths per 1e6 Population", "value": "deaths_daily_1e6_pop"},
                                {"label": "Daily Recovered per 1e6 Population", "value": "recovered_daily_1e6_pop"},
                                {"label": "Cumulative Cases per 1e6 Population", "value": "cases_cumulative_1e6_pop"},
                                {"label": "Cumulative Deaths per 1e6 Population", "value": "deaths_cumulative_1e6_pop"},
                                {"label": "Cumulative Recovered per 1e6 Population", "value": "recovered_cumulative_1e6_pop"},
                                {"label": "Population", "value": "country_population"}
                            ],
                            value = "cases_daily",
                            inline = False,
                            style = {"text-align": "left",
                                     "font-size": "1.2rem"}
                        ),
                        width = 3
                    )
                ]
            )
                
        ]
    )
    return(ui_block)

