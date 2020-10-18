
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from Funcs.default_params import spinner_type, cards_colors

def ui_card_totals(title,
                   content):
    
    """
    Card to display the total numbers of cases, deaths ou recovered.
    """
    
    type = ""
    if "cases" in title.lower():
        type = "cases"
    if "deaths" in title.lower():
        type = "deaths"
    if "recovered" in title.lower():
        type = "recovered"
    
    card = dbc.Card(
            dbc.CardBody(
                [
                    html.H3(content,
                            className = "card-title"),
                    html.Br(),
                    html.H5(title,
                            className = "card-subtitle")
                ]
            ),
            className = "card_totals_color_" + type,
            color = cards_colors[type],
            inverse = False
    )
    return(card)

