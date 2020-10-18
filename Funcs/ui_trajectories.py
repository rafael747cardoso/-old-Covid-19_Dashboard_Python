
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Funcs.default_params import spinner_type, cards_colors, period_options, countries_options

def ui_trajectories(type):

    """
    UI for the trajectories plot with scale and the country and moving average dropdowns.
    """

    ui_block = dcc.Loading(
        id = "loading_trajectories_" + type,
        type = spinner_type,
        children = 
            [
                dbc.Card(
                    [
                        dbc.CardHeader(type.title()),
                        dbc.CardBody(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Br(),
                                                html.H4("Select the countries:",
                                                        style = {"margin-left": "1.5rem"}),
                                                html.Br(),
                                                dcc.Dropdown(
                                                    id = "chosen_countries_trajectories_" + type,
                                                    className = "dash-bootstrap",
                                                    options = countries_options,
                                                    value = [countries_options[0]["value"]],
                                                    multi = True,
                                                    style = {"width": "90%",
                                                             "margin-left": "1.3rem"}
                                                )
                                            ],
                                            width = 6
                                        ),
                                        dbc.Col(
                                            [
                                                html.Br(),
                                                html.H4("Choose the period of the moving average:",
                                                        style = {"margin-left": "1.5rem"}),
                                                html.Br(),
                                                dcc.Dropdown(
                                                    id = "chosen_period_trajectories_" + type,
                                                    className = "dash-bootstrap",
                                                    options = period_options,
                                                    value = period_options[0]["value"],
                                                    style = {"width": "90%",
                                                             "margin-left": "1.3rem"}
                                                )
                                            ],
                                            width = 6
                                        )
                                    ]
                                ),
                                html.Br(),
                                dbc.RadioItems(
                                    id = "scale_trajectories_" + type,
                                    options = 
                                        [
                                            {"label": "Linear", "value": False},
                                            {"label": "Log", "value": True}
                                        ],
                                    value = False,
                                    inline = True,
                                    style = {"text-align": "center"}
                                ),
                                dcc.Graph(id = "plot_trajectories_" + type,
                                          figure = {})
                            ]
                        )
                    ],
                    className = "card_header_color_" + type,
                    color = cards_colors[type],
                    outline = True,
                    inverse = True
                )
            ]
        )
    return(ui_block)

