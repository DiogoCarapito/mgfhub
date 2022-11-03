import dash
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(__name__,
                   path='/',
                   title='Dashboard Indicadores',
                   name='Dashboard'
                )

df = pd.read_csv('scrapped_indicadores.csv')
df.drop(columns=df.columns[0], axis=1, inplace=True)

#table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])
table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True)

container_1 = dbc.Container([
    html.H3('Dashboard'),
    table
])

layout = html.Div([
    container_1,
    html.Br(),
])