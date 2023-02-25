import dash
import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, callback, Input, Output

dash.register_page(
    __name__,
    path='/home',
    title='home',
    name='home',
    order=0,
)

searchbox = html.Div([
    dbc.Input(
        id='searchbox',
        placeholder='search...',
        type='text',
        size='lg',
    ),
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
    return search