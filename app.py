import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px

from dash.dependencies import Input, Output

# initialize app

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# load data

df_confirmed = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
)
df_deaths = pd.read_csv(
    "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
)

df_tc = (
    pd.DataFrame(df_confirmed.iloc[:, 4:].sum())
    .reset_index()
    .rename(columns={"index": "Date", 0: "Confirmed"})
)

df_td = (
    pd.DataFrame(df_deaths.iloc[:, 4:].sum())
    .reset_index()
    .rename(columns={"index": "Date", 0: "Deaths"})
)

df_countries = df_confirmed.groupby(["Country/Region"]).sum().iloc[:, -1].reset_index()

# app layout

graph_c = html.Div(
    [
        dcc.Graph(
            id="graph_confirmed",
            figure=px.line(data_frame=df_tc, x="Date", y="Confirmed"),
        )
    ]
)

graph_d = html.Div(
    [
        dcc.Graph(
            id="graph_deaths", figure=px.line(data_frame=df_td, x="Date", y="Deaths")
        )
    ]
)


app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H2("Global Coronavirus/COVID-19 Cases"),
                        html.P("Select a country below."),
                        html.Div(
                            className="div-for-dropdown",
                            children=[
                                dcc.Dropdown(
                                    id="country-picker",
                                    options=[
                                        {"label": country, "value": country}
                                        for country in sorted(
                                            df_confirmed["Country/Region"].unique()
                                        )
                                    ],
                                    value="US",
                                ),
                                html.P(id="dd-output"),
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
                                data_frame=df_countries,
                                locations="Country/Region",
                                hover_name="Country/Region",
                                color=df_countries.columns[-1],
                                locationmode="country names",
                                color_continuous_scale=px.colors.sequential.OrRd,
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
    return f"You have selected {value}"


# update line graph for selected country
@app.callback(Output("line", "figure"), [Input("country-picker", "value")])
def update_line(country):
    df_country = (
        df_confirmed[df_confirmed["Country/Region"] == country]
        .iloc[:, 4:]
        .T.sum(axis=1)
        .reset_index()
    )
    df_country.columns = ["Date", "Confirmed"]
    return px.line(data_frame=df_country, x="Date", y="Confirmed")


# run app

if __name__ == "__main__":
    app.run_server(debug=True)
