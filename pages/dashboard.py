import dash
from dash import Dash, dcc, html, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(
    __name__,
    path='/',
    title='dashboard indicadores',
    name='dashboard',
    order=1,
)

df_todos_indicadores = pd.read_csv('data/scrapped_indicadores.csv')
usf_ucsp_para_idg = pd.read_csv('data/usf_ucsp_indicadores_2022_comimpactoIDG.csv')
#usf_ucsp_sem_idg = pd.read_csv('data/usf_ucsp_indicadores_2022_semimpactoIDG.csv')

df_todos_indicadores_filtered = df_todos_indicadores[df_todos_indicadores['id'].isin(usf_ucsp_para_idg['indicador'].values.tolist())]


#df_todos_indicadores = pd.read_csv('/home/diogocarapito/bi_indicadores/data/scrapped_indicadores.csv')
#df_todos_indicadores.drop(columns=df_todos_indicadores.columns[0], axis=1, inplace=True)

#table = dash_table.DataTable(df_todos_indicadores.to_dict('records'), [{"name": i, "id": i} for i in df_todos_indicadores.columns])



table = dbc.Table.from_dataframe(
    df_todos_indicadores_filtered,
    striped=True,
    bordered=True,
    hover=False,
    id='tabela_indicadores'
)


table_filters = ['todos','USF/UCSP com impacto IDG','USF/UCSP sem impacto IDG',]

filters = html.Div([
    dbc.Row([
        dbc.Col([
            dcc.RadioItems(
                options=table_filters,
                value=table_filters[0],
                inline=True,
                id='radio_tabela')
        ])
    ])
])

container_1 = dbc.Container([
    html.H3('dashboard'),
    html.Br(),
    filters,
    table,
],fluid=True,)


def layout():
    return html.Div([
        dbc.Row([
            dbc.Col([
                container_1,
                html.Br(),
            ],width={"size": 10, "offset": 0},)
        ])

    ])


'''@callback(
    Output('tabela_indicadores', 'children'),
    Input('radio_tabela', 'value'),
)


def table_update(radio_tabela):

    if radio_tabela == 'Todos':
        df_todos_indicadores_novo = df_todos_indicadores
    elif radio_tabela == 'USF/UCSP com impacto IDG':
        df_todos_indicadores_novo = df_todos_indicadores
    elif radio_tabela == 'USF/UCSP sem impacto IDG':
        df_todos_indicadores_novo = df_todos_indicadores
    tabela_indicadores = dash_table.DataTable(

    )

    return tabela_indicadores'''