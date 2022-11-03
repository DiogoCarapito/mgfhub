import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import csv

dash.register_page(__name__,
                   path='/about',
                   title='About',
                   name='About')


container_1 = dbc.Container([
    html.H3('about'),
    ])

layout = html.Div([
    container_1,
    html.Br(),
])