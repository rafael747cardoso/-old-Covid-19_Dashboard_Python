
import plotly.express as px

def plot_ts(df,
            y_var,
            y_scale,
            type_color):
    
    """
    General plot for a time series.
    """
    
    y_name = y_var.split("_")
    if y_name[1] == "cum":
        y_name[1] = "Cumulative"
    y_name = y_name[1].title() + " " + y_name[0].title()
    
    p = px.line(
        data_frame = df,
        x = "date",
        y = y_var,
        color_discrete_sequence = [type_color],
        template = "plotly_dark",
        log_y = y_scale,
        labels = {"date": "Date",
                  y_var: y_name}
    )
    return(p)

