import os

import dash
import dash_core_components as dcc
import dash_html_components as html

import pandas as pd

# initialize app

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

# load data

df_confirmed = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
df_deaths = pd.read_csv('https://github.com/CSSEGISandData/COVID-19/blob/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')

df_total = pd.DataFrame(df.iloc[:, 4:].sum()).reset_index().rename(columns = {'index': 'Date', 0: 'Confirmed'})

# app layout

graph = dcc.Graph(
            id = 'selected-datate',
            figure = px.line( data_frame = df_total, x = 'Date', y = 'Confirmed' ))

app.layout = html.Div([
    html.H2('Hello World'),
    dcc.Dropdown(
        id='dropdown',
        options=[{'label': i, 'value': i} for i in ['LA', 'NYC', 'MTL']],
        value='LA'
    ),
    html.Div(id='display-value'),
    graph
])

# callbacks

@app.callback(dash.dependencies.Output('display-value', 'children'),
              [dash.dependencies.Input('dropdown', 'value')])
def display_value(value):
    return 'You have selected "{}"'.format(value)

# run app

if __name__ == '__main__':
    app.run_server(debug=True)
