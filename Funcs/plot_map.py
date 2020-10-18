
import numpy as np
import pandas as pd
import plotly.express as px

def plot_map(df,
             var):
    
    """
    General choropleth map for the world's countries.
    """

    color_scale = "Jet"
    if "cases" in var:
        color_scale = "Blues"
    if "deaths" in var:
        color_scale = "Reds"
    if "recovered" in var:
        color_scale = "Greens"

    df[var + "_log"] = np.log10(df[var])
    var_used = var + "_log"
    hover_dict = {"alpha_3": False,
                  var_used: False,
                  var: ":.0f"}
    if "1e6_pop" in var:
        hover_dict = {"alpha_3": False,
                      var_used: False,
                      var: ":.0f"}

    map = px.choropleth(data_frame = df,
                        locations = "alpha_3",
                        color = var_used,
                        color_continuous_scale = color_scale,
                        hover_name = "country",
                        hover_data = hover_dict,
                        template = "plotly_dark",
                        projection = "natural earth")
    map.update_layout(coloraxis_colorbar = {"title": var.title().replace("_", " "),
                                            "tickprefix": "1.e"},
                      height = 700)
    return(map)

