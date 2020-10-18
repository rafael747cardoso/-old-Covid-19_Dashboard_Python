
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Funcs.default_params import spinner_type, cards_colors

def ui_ts_plot(plot_ids):
    
    """
    Defines the UI of the block with the Time Series plot and scale.
    """
    
    type = ""
    if "cases" in plot_ids:
        type = "cases"
    if "deaths" in plot_ids:
        type = "deaths"
    if "recovered" in plot_ids:
        type = "recovered"
    
    ui_block = [   
        dbc.Card(
            [
                dbc.CardHeader(type.title()),
                dbc.CardBody(
                    [
                        dbc.RadioItems(
                            id = "scale_" + plot_ids,
                            options = 
                                [
                                    {"label": "Linear", "value": False},
                                    {"label": "Log", "value": True}
                                ],
                            value = False,
                            inline = True,
                            style = {"text-align": "center"}
                        ),
                        dcc.Loading(
                            id = "loading_plot_" + plot_ids,
                            type = spinner_type,
                            children = [
                                dcc.Graph(id = "plot_" + plot_ids,
                                          figure = {}),
                            ]
                        )
                    ]
                )
            ],
            className = "card_header_color_" + type,
            color = cards_colors[type],            
            outline = True,
            inverse = True
        )
    ]
    return(ui_block)

