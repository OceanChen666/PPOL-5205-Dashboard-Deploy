from dash import Dash, dcc, html, Input, Output
import pandas as pd
import plotly.express as px

mydataset = "https://raw.githubusercontent.com/OceanChen666/PPOL-5205-Concept-Showcase/main/platform.csv"

df = pd.read_csv(mydataset)
df.dropna(inplace=True)


app = Dash(__name__)
server = app.server


app.layout = html.Div([
    html.Header("Offshore Platform Dash App", style={"fontSize": 40,
                                               "textAlign": "center"}),
    dcc.Dropdown(id="mydropdown",
                 options=['kmeans_label','ahc_label','dbscan_label'],
                 value="",
                 style={"width": "50%", "margin-left": "130px", "margin-top": "60px"}),
    dcc.Graph(id="my_scatter_geo")
])


@app.callback(Output("my_scatter_geo", "figure"),
              Input("mydropdown", "value"))
def sync_input(cluster_selection):
    fig = px.scatter_geo(df, 
                     lat='LATITUDE', 
                     lon='LONGITUDE',  
                     color=cluster_selection,
                        #    color="peak_hour", size="car_hours",
                  hover_name="OPERNAME")
    # Set Size of Dots
    fig.update_traces(marker=dict(size=2.5))
    # Layout
    fig.update_geos(
        visible=False, # hides default base map 
        showcountries=True, 
        lonaxis_range=[-98, -84],  # longitude range
        lataxis_range=[26, 30],    # latitude range
    )
    fig.update_layout(
        title = f'Aged US offshore platform{cluster_selection}',
        geo=dict(
        scope='north america',
        showland=True,
        landcolor="rgb(212, 212, 212)",
        countrycolor="rgb(255, 255, 255)"
    ))
    return fig


if __name__ == "__main__":
    app.run_server(debug=False)
