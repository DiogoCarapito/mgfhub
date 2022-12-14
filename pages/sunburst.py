import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import numpy as np
import re

dash.register_page(
    __name__,
    path='/sunburst',
    title='sunburst',
    name='sunburst',
    order=3,
)

df_sunburst = pd.read_csv('data/sunburst_data.csv')

table_filters = ['todos', 'USF/UCSP com impacto IDG', 'USF/UCSP sem impacto IDG']
filters = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(
                options=table_filters,
                value=table_filters[0],
                inline=True,
                id='radio_tabela'
            )
        ])
    ])
])


header = html.Div((
    dbc.Row([
        html.H3('sunburst'),
    ]),
))

graphs = html.Div([
    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            dcc.Graph(id='sunburstindicadores')
        ], width=10),
        dbc.Col([], width=1),
    ]),
    dbc.Row([
        html.Div(id='test_container'),
    ])
])

container = dbc.Container([
    dbc.Row([
        dbc.Col([
            header,
            filters,
            html.Br(),
            graphs,
        ])
    ])
], fluid=True)


def layout():
    return html.Div([
        container,
        html.Br(),
    ])


@callback(
    Output('sunburstindicadores', 'figure'),
    #Output('sunburst', 'figure'),
    Input('radio_tabela', 'value'),
)

def sunburst_update(radio_tabela):

    fig_sunburstindicadores = go.Figure()
    fig_sunburstindicadores.add_trace(go.Sunburst(
        ids=df_sunburst.id,
        labels=df_sunburst.label,
        parents=df_sunburst.parent,
        values=df_sunburst.value,
        branchvalues="total",
        domain=dict(column=1),
        insidetextorientation='radial',
    ))
    fig_sunburstindicadores.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        width=800,
        height=800,
    )

    return fig_sunburstindicadores


@callback(
    Output('test_container', 'children'),
    Input('store_data', 'data'),
)

def stora_data_show(data):
    if data is None:
        return
    else:
        df=pd.DataFrame(data)
        print(df)
        return html.Div([
                html.H1(['SUCCESS']),
            ])

