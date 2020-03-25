import os

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

import plotly.express as px

# initialize app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# load data

df_confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
df_deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

df_tc = pd.DataFrame(df_confirmed.iloc[:, 4:].sum()).reset_index().rename(columns = {'index': 'Date', 0: 'Confirmed'})
df_td = pd.DataFrame(df_confirmed.iloc[:, 4:].sum()).reset_index().rename(columns = {'index': 'Date', 0: 'Deaths'})


# app layout

graph_c = html.Div([dcc.Graph(id = 'graph_confirmed',
                                      figure = px.line( data_frame = df_tc, x = 'Date', y = 'Confirmed' ))])

graph_d = html.Div([dcc.Graph(id = 'graph_deaths',
                                      figure = px.line( data_frame = df_td, x = 'Date', y = 'Deaths' ))])


app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value'),
    graph_c,
    graph_d
])

# callbacks

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

# run app

if __name__ == '__main__':
    app.run_server(debug=True)
