import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__,
                   path='/',
                   title='Dashboard Indicadores',
                   name='Dashboard'
                )


layout = html.Div([
    html.Br(),
    dbc.Container([
        html.H3('dashboard')
    ])
])
