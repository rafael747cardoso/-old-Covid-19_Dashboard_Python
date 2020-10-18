
import numpy as np
import pandas as pd
import plotly.express as px

def plot_trajectories(df,
                      type_var,
                      period,
                      scale):
    
    """
    General plot for the trajectories.
    """
    
    # Moving average:
    countries = df["country_code"].unique()    
    df_mean = pd.DataFrame({type_var + "_cum": [],
                            type_var + "_daily": [],
                            "country_code": [],
                            "country": []})
    for c in countries:
        dfi = df.iloc[np.where(df["country_code"] == c)]
        dfi = dfi.rolling(window = period).mean()
        dfi["country_code"] = c
        dfi["country"] = df["country"].iloc[np.where(df["country_code"] == c)[0]]
        df_mean = df_mean.append(dfi)

    p = px.line(
        data_frame = df_mean,
        x = type_var + "_cum",
        y = type_var + "_daily",
        color = "country",
        template = "plotly_dark",
        log_x = scale,
        log_y = scale,
        labels = {type_var + "_cum": "Cumulative " + type_var.title(),
                  type_var + "_daily": "Daily " + type_var.title()},
        hover_name = "country",
        hover_data = {type_var + "_cum": ":.0f",
                      type_var + "_daily": ":.0f",
                      "country_code": False,
                      "country": False}
    )
    return (p)

