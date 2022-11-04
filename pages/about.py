import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import csv

dash.register_page(
    __name__,
    path='/about',
    title='About',
    name='About',
    order=3,
)


container_1 = dbc.Container([
    html.H3('about'),
    ],fluid=True,)

def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])