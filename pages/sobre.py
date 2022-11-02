import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

dash.register_page(__name__,
                   path='/sobre',
                   title='Sobre',
                   name='Sobre'
)

df = px.data.tips()

layout = html.Div([
    html.Br(),
    dbc.Container([
        html.H3('sobre')
    ])
])