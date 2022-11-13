import dash
from dash import Dash, dcc, html, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
#import plotly.graph_objects as go
from rapidfuzz import process, fuzz

dash.register_page(
    __name__,
    path='/',
    title='indicadores',
    name='indicadores',
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


s=' '
df_todos_indicadores = df_todos_indicadores.assign(indexing=[str(row.id)+s+row.nome_abreviado+s+row.designacao+s+str(row.area)+s+str(row.subarea)+s+str(row.dimensao)+s+row.tipo_de_indicador+s+row.area_clinica for index, row in df_todos_indicadores.iterrows()])


'''
s=' '
df_search_indexing = pd.DataFrame([
    {'indexing': str(row.id)+s+row.nome_abreviado+s+row.designacao+s+row.objetivo+s+str(row.area)+s+str(row.subarea)+s+str(row.dimensao)+s+row.tipo_de_indicador+s+row.area_clinica
    } for index, row in df_todos_indicadores.iterrows()
])

df_todos_indicadores = pd.concat([df_todos_indicadores,df_search_indexing])
'''

#[str(row.id)+s+row.nome_abreviado+s+row.designacao+s+row.objetivo+s+str(row.area)+s+str(row.subarea)+s+str(row.dimensao)+s+row.tipo_de_indicador+s+row.area_clinica for index, row in df.iterrows()]

'''
# Filtragem dos indicadores que contam apenas para o IDG das USF E USCP
df = df_todos_indicadores[df_todos_indicadores['id'].isin(usf_ucsp_para_idg['indicador'].values.tolist())]

# Simplificação da tabela, deixando cair colunas não importantes para mostrar
df = df.drop(columns=['codigo','codigo_siars','nome_abreviado','objetivo','formula','unidade_de_medida', 'output','estado_do_indicador','inclusao_de_utentes_no_indicador','prazo_para_registos','link'])
'''

# objeto para entrar no HT
table = dash_table.DataTable(
    id='tabela_indicadores',
    page_size=448,
    sort_action="native",
    #filter_action='native',
    style_header={
        'backgroundColor': 'rgb(240, 240, 240)',
        'fontWeight': 'bold'
    },
    style_cell={
        'padding': '5px',
        'textAlign': 'left',
        'height': 'auto',
        #'minWidth': '30px', 'width': '30px','maxWidth': '360px',
        'whiteSpace': 'normal',
        },
    style_data={'whiteSpace': 'normal','height': 'auto',},
    style_table={'overflowX': 'auto'},
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)',
        }
    ],
)

search_box = html.Div([
    dbc.Input(
        id='searchbox',
        placeholder='search...',
        type='text',
        size='sm',
    ),
])

radio_options=[
    {'label':'USF/UCSP com impacto IDG','value':'USF/UCSP com impacto IDG'},
    {'label':'USF/UCSP sem impacto IDG','value':'USF/UCSP sem impacto IDG'},
    {'label':'todos','value':'todos'},
]
radio = html.Div([
    dbc.RadioItems(
        options=radio_options,
        value='USF/UCSP com impacto IDG',
        inline=True,
        id='radio_tabela'
    )
])

filters = html.Div([
    dbc.Row([
        dbc.Col([
            search_box,
        ], width=3),
        dbc.Col([
            radio,
        ], width=9),
    ])
])

contagem = html.Div([html.P(id='contagem_indicadores')],style={'padding': '12px 0px 0px 4px'})

container_1 = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3('indicadores'),
            html.Br(),
            filters,
            contagem,
            table,
        ])
    ])
], fluid=True)


def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])


@callback(
    Output('tabela_indicadores', 'data'),
    Output('tabela_indicadores', 'columns'),
    Output('contagem_indicadores','children'),
    Input('searchbox', 'value'),
    Input('radio_tabela', 'value'),
)


def table_update(searchbox,radio_tabela):
    
    df_indicadores_novo = df_todos_indicadores
    if radio_tabela == 'Todos':
        df_indicadores_novo = df_todos_indicadores
    elif radio_tabela == 'USF/UCSP com impacto IDG':
        df_indicadores_novo = df_todos_indicadores[
            df_todos_indicadores['id'].isin(usf_ucsp_para_idg['indicador'].values.tolist())]
    elif radio_tabela == 'USF/UCSP sem impacto IDG':
        df_indicadores_novo = df_todos_indicadores[
            df_todos_indicadores['id'].isin(usf_ucsp_sem_idg['indicador'].values.tolist())]
    
    if searchbox == None or searchbox == '':
        df_after_search = df_indicadores_novo
    else:
        search_list = process.extract(searchbox, df_indicadores_novo.indexing, scorer=fuzz.WRatio, score_cutoff=59, limit=50)
        df_after_search = df_indicadores_novo.filter([id[2] for id in search_list], axis=0)

        print(search_list)
        print(len([id[2] for id in search_list]))
        print([id[1] for id in search_list])

    df_after_search = df_after_search.drop(columns=['codigo', 'codigo_siars', 'nome_abreviado','objetivo', 'formula', 'unidade_de_medida', 'output','estado_do_indicador', 'inclusao_de_utentes_no_indicador', 'prazo_para_registos', 'link','indexing'])

    df_data = df_after_search.to_dict('records')
    df_columns = [{"name": i, "id": i} for i in df_after_search.columns]


    return df_data,df_columns,str(len(df_after_search))+' indicadores'
