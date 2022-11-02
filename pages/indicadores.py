import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px

dash.register_page(__name__,
                   path='/indicadores',
                   title='Indicadores',
                   name='Indicadores'
)

df = px.data.tips()

layout = html.Div([
    html.Br(),
    dbc.Container([
        dcc.RadioItems([x for x in df.day.unique()], id='day-choice'),
        dcc.Graph(id='bar-fig',
                  figure=px.bar(df, x='smoker', y='total_bill'))
    ])
])