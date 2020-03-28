import os
import dash
import datetime
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

from dash.dependencies import Input, Output, State

# initialize app
app = dash.Dash(__name__)

server = app.server

# load data

df = pd.read_csv(
    "https://raw.githubusercontent.com/datasets/covid-19/master/data/countries-aggregated.csv",
    parse_dates=["Date"],
)

# Datetime string feature for animation frames
df["Date_Str"] = df["Date"].dt.strftime("%m-%d")

dropdown_options = [
    {"label": country, "value": country} for country in sorted(df["Country"].unique())
]

# app layout

app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("Global Coronavirus Cases"),
                        html.P("Select a country below."),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id="country-picker",
                                    options=dropdown_options,
                                    value="US",
                                ),
                                html.P(id="dd-output"),
                                dcc.Markdown(
                                    children=[
                                        "Source: [DataHub](https://datahub.io/core/covid-19)"
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(
                            id="map-graph",
                            figure=px.choropleth(
                                data_frame=df[df["Date"] >= pd.Timestamp(2020, 3, 1)],
                                locations="Country",
                                hover_name="Country",
                                color="Confirmed",
                                locationmode="country names",
                                color_continuous_scale=px.colors.sequential.Reds,
                                template="plotly_dark",
                                animation_frame="Date_Str",
                            ),
                        ),
                        dcc.Graph(id="line"),
                    ],
                ),
            ],
        )
    ]
)

# callbacks

# update selected Country
@app.callback(
    Output("dd-output", "children"), [Input("country-picker", "value")],
)
def update_output(value):
    return ""

# if country selected, clear click data
@app.callback(Output("map-graph", "clickData"), [Input("country-picker", "value")])
def update_selected_data(country):
    if country:
        return None

# update line graph for selected country
@app.callback(
    Output("line", "figure"),
    [Input("country-picker", "value"), Input("map-graph", "clickData")],
)
def update_line(country, choro_click):

    if choro_click != None:
        country = choro_click["points"][0]["location"]

    return px.line(
        data_frame=df[df["Country"] == country],
        x="Date",
        y="Confirmed",
        template="plotly_dark",
    )


# run app

if __name__ == "__main__":
    app.run_server(debug=True)
