import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/home',
    title='home',
    name='home',
    order=0,
)

container_1 = dbc.Container([
    html.H3('Hello world!'),
], fluid=True)


def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])

