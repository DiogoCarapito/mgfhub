import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import numpy as np

dash.register_page(
    __name__,
    path='/sunburst',
    title='sunburst',
    name='sunburst',
    order=3,
)
''''
table_filters = ['todos', 'USF/UCSP com impacto IDG', 'USF/UCSP sem impacto IDG']
filters = dbc.Container([
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
'''

header = dbc.Container((
    dbc.Row([
        html.H3('sunburst'),
    ]),
))


container = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sunburst')
        ], width=6),
        dbc.Col([

        ], width=6),
    ]),
], fluid=True)


def layout():
    return html.Div([
        header,
        #filters,
        container,
        html.Br(),
    ])


@callback(
    Output('sunburst', 'figure'),
    #Input('radio_tabela', 'value'),
)

def sunburst_update(radio_tabela):
    '''
    df_todos_indicadores_novo = df_todos_indicadores
    if radio_tabela == 'Todos':
        df_todos_indicadores_novo = df_todos_indicadores
    elif radio_tabela == 'USF/UCSP com impacto IDG':
        df_todos_indicadores_novo = df_todos_indicadores[df_todos_indicadores['id'].isin(usf_ucsp_para_idg['indicador'].values.tolist())]
    elif radio_tabela == 'USF/UCSP sem impacto IDG':
        df_todos_indicadores_novo = df_todos_indicadores[df_todos_indicadores['id'].isin(usf_ucsp_sem_idg['indicador'].values.tolist())]

    df_todos_indicadores_novo_colmun = [{"name": i, "id": i} for i in df_todos_indicadores_novo.columns]
    '''

    df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/coffee-flavors.csv')

    fig = go.Figure()

    fig.add_trace(go.Sunburst(
        ids=df.ids,
        labels=df.labels,
        parents=df.parents,
        domain=dict(column=1),
        maxdepth=2,
        insidetextorientation='radial'
    ))

    fig.update_layout(
        margin=dict(t=10, l=10, r=10, b=10)
    )


    return fig
