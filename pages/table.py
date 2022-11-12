import dash
from dash import Dash, dcc, html, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from rapidfuzz import process, fuzz

dash.register_page(
    __name__,
    path='/',
    title='tabela indicadores',
    name='tabela',
    order=1,
)

# read_csv read no PyCharm!!
pythonanywhere_file_tree = ''
#pythonanywhere_file_tree = '/home/diogocarapito/bi_indicadores/'

# Laod da principal base de dados em .csv
df_todos_indicadores = pd.read_csv(pythonanywhere_file_tree + 'data/scrapped_indicadores.csv')
# Load das listas de id's de indicadores utilizados para IDG
usf_ucsp_para_idg = pd.read_csv(pythonanywhere_file_tree + 'data/usf_ucsp_indicadores_2022_comimpactoIDG.csv')
usf_ucsp_sem_idg = pd.read_csv(pythonanywhere_file_tree + 'data/usf_ucsp_indicadores_2022_semimpactoIDG.csv')

# Filtragem dos indicadores que contam apenas para o IDG das USF E USCP
df = df_todos_indicadores[df_todos_indicadores['id'].isin(usf_ucsp_para_idg['indicador'].values.tolist())]

# Simplificação da tabela, deixando cair colunas não importantes para mostrar
df = df.drop(columns=['codigo','codigo_siars','nome_abreviado','objetivo','formula','unidade_de_medida', 'output','estado_do_indicador','inclusao_de_utentes_no_indicador','prazo_para_registos','link'])

# objeto para entrar no HT
table = dash_table.DataTable(
    id='tabela_indicadores',
    data = df.to_dict('records'),
    columns = [{"name": i, "id": i} for i in df.columns],
    page_size=448,
    style_cell={'textAlign': 'left'}
)

search_box = html.Div([
    dbc.Input(id='searchbox', placeholder='', type='text'),
])

container_1 = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3('tabela'),
            html.Br(),
            search_box,
            table,
        ])
    ])
], fluid=True,)


def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])


@callback(
    Output('tabela_indicadores', 'data'),
    Output('tabela_indicadores', 'columns'),
    Input('searchbox', 'value'),
)


def table_update(searchbox):
    print(type(searchbox))
    if searchbox == None:
        df_after_search = df
    else:
        if searchbox.isnumeric():
            search_list = process.extract(searchbox,df.id,scorer=fuzz.ratio,score_cutoff=99)
        else:
            search_list = process.extract(searchbox, df.designacao,scorer=fuzz.WRatio,score_cutoff=20)
            #search_list = process.extract(searchbox, df.designacao, scorer=fuzz.WRatio, limit=20)
            #search_list = process.extract(searchbox, df.designacao, scorer=fuzz.token_sort_ratio, score_cutoff=50)

        df_after_search = df.filter([id[2] for id in search_list], axis=0)

        print(search_list)
        print([id[2] for id in search_list])
        print([id[1] for id in search_list])
    df_data = df_after_search.to_dict('records')
    df_columns = [{"name": i, "id": i} for i in df_after_search.columns]

    return df_data,df_columns
