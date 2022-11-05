import dash
from dash import Dash, dcc, html, dash_table
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(
    __name__,
    path='/',
    title='dashboard indicadores',
    name='dashboard',
    order=1,
)

df = pd.read_csv('csv_test.csv')
#df = pd.read_csv('data/scrapped_indicadores.csv')
#df.drop(columns=df.columns[0], axis=1, inplace=True)

#table = dash_table.DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

df = pd.DataFrame([1,2,3,4,5,6])

table = dbc.Table.from_dataframe(
    df,
    striped=True,
    bordered=True,
    hover=False,
    id='tabela_indicadores'
)

#usf_ucsp_para_idg = pd.read_csv('data/usf_ucsp_indicadores_2022_comimpactoIDG.csv')
#usf_ucsp_sem_idg = pd.read_csv('data/usf_ucsp_indicadores_2022_semimpactoIDG.csv')

table_filters = ['todos','USF/UCSP com impacto IDG','USF/UCSP sem impacto IDG',]

'''
df = pd.DataFrame([1,2])
table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=False)
'''
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
    Output('tabela_indicadores', 'figure'),
    Input('radio_tabela', 'value'),
)'''

'''
def table_update(radio_tabela):

    if radio_tabela == 'Todos':
        df_novo = df
    elif radio_tabela == 'USF/UCSP com impacto IDG':
        df_novo = df
    elif radio_tabela == 'USF/UCSP sem impacto IDG':
        df_novo = df
    tabela_indicadores = dbc.Table.from_dataframe(
        df_novo,
        striped=True,
        bordered=True,
        hover=False,
        id='tabela_indicadores'
    )

    return tabela_indicadores'''