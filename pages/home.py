import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_excel('data.xlsx', header=2)

dash.register_page(__name__,
                   path='/',
                   title='Dashboard Indicadores',
                   name='Dashboard')

dashboard = dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Row([
                    dcc.Graph(
                        id='sunburst_indicadores',
                        figure=px.sunburst(
                            df,
                            path=['Hierarquia Contratual - Sub-Área', 'Hierarquia Contratual - Dimensão','Designação Indicador (+ID)'],
                            values='Score'
                        )
                    )
                ]),
                dbc.Row([
                    html.Div([html.H3('Home')])
                ]),
            ], width=8),
            dbc.Col([
                dbc.Row([
                    html.Div([html.H3('Home')])
                ]),
            ], width=2),
            dbc.Col([
                dbc.Row([
                    html.Div([html.H3('Home')])
                ]),
            ], width=2),
        ])
    ])

layout = html.Div([
    html.Br(),
    dashboard
])
