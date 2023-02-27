import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, callback, Input, Output

import requests



dash.register_page(
    __name__,
    path='/home',
    title='home',
    name='home',
    order=1,
)

searchbox = html.Div([
    dbc.Input(
        id='searchbox',
        placeholder='search...',
        type='text',
        size='lg',
    ),
    dbc.Button("Ask", color="secondary", className="me-1"),
])

responses = html.Div([],id='responses')

container_1 = dbc.Container([
    html.Br(),
    searchbox,
    html.Br(),
    responses
], fluid=True)


def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])

@callback(
    Output('responses', 'children'),
    Input('searchbox', 'value'),
)

def search_query(search):
    if search == None:
        return None
    else:
        response = requests.post("https://mrjiggy-model1.hf.space/run/predict", json={
            "data": [search]
        }).json()

        data = response["data"]
        return data