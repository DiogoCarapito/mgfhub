import dash
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__,
                   path='/',
                   title='Dashboard Indicadores',
                   name='Dashboard'
                )

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')
table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

container_1 = dbc.Container([
    html.H3('Dashboard'),
    table
])

layout = html.Div([
    container_1
])