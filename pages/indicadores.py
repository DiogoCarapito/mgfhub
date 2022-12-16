import dash
from dash import Dash, dcc, html, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
#import plotly.graph_objects as go
from rapidfuzz import process, fuzz

dash.register_page(
    __name__,
    path='/indicadores',
    title='indicadores',
    name='indicadores',
    order=2,
)

# read_csv read no PyCharm!!
## tem que ser mudado para link do github para funcionar cross platform
pythonanywhere_file_tree = ''
#pythonanywhere_file_tree = '/home/diogocarapito/bi_indicadores/'

# Laod da principal base de dados em .csv
## Ponderar fazer um script para adicionar informação sobre Intervalos aceitáveis ideias a partir do PDF da Operacionalização da ACSS
## Terminar o scrapper sdm, porquen ainda falta infomração de formula de calculo
df_todos_indicadores = pd.read_csv(pythonanywhere_file_tree + 'data/scrapped_indicadores.csv')

# Load das listas de id's de indicadores utilizados para IDG das USFs/UCSPs
## podem vir a ser adicionados a lista de indicadores doas UCC, USP, ACES
## eventualmente tem que se escrever um script para extrair diretamente do PDF da Operacionalização da ACSS
usf_ucsp_para_idg = pd.read_csv(pythonanywhere_file_tree + 'data/usf_ucsp_indicadores_2022_comimpactoIDG.csv')
usf_ucsp_sem_idg = pd.read_csv(pythonanywhere_file_tree + 'data/usf_ucsp_indicadores_2022_semimpactoIDG.csv')

# Load dos intervalos aceitávels e esperados
df_intervalos = pd.read_csv(pythonanywhere_file_tree + 'data/scrapped_intervalos.csv')
df_todos_indicadores = df_todos_indicadores.merge(df_intervalos, on="id",how="outer")
df_todos_indicadores.fillna(np.nan, inplace=True)

# Criação de uma coluna com concatonação da info importante para o algoritmo de pesquiza pelo método fuzzy
# Algumas celulas têm que ser
s=' '
df_todos_indicadores = df_todos_indicadores.assign(
    indexing=[
        str(row.id) + s
        + row.nome_abreviado + s
        + row.designacao+s+str(row.area) + s
        + str(row.subarea) + s
        + str(row.dimensao) + s
        + row.tipo_de_indicador + s
        + row.area_clinica
        for index, row in df_todos_indicadores.iterrows()])

# Markdown para ter um link na tabela
df_todos_indicadores = df_todos_indicadores.assign(
    id_sdm = [
        '['
        + str(row['id'])
        + ']('
        + row['link']
        + ')'
        for index, row in df_todos_indicadores.iterrows()])

'''dbc.Table([
                                    html.Thead([
                                        html.Th('área'),
                                        html.Th('subarea'),
                                        html.Th('dimensao')
                                    ]),
                                    html.Tbody([
                                        html.Tr([
                                            html.Td(indicador[1]['area']),
                                            html.Td(indicador[1]['subarea']),
                                            html.Td(indicador[1]['dimensao']),
                                        ]),
                                    ])
                                ]),'''

def generate_html_indicador(indicador):
    separador = ' - '
    return dbc.Container([
        dbc.Card([
            dbc.CardHeader(children=html.H4([str(indicador[1][0]) + separador + indicador[1][1]])),
            dbc.CardBody([
                dbc.Container([
                    dbc.Row([
                        dbc.Col([
                            dbc.Row([
                                html.B([str(indicador[1]['area']) + ' > ' + str(indicador[1]['subarea']) + ' > ' + str(indicador[1]['dimensao'])])
                            ]),
                            html.Br(),
                            dbc.Row([
                                html.P([indicador[1]['objetivo']]),
                                html.A('link SDM', href=indicador[1]['link']),
                            ]),

                        ],width=7),
                        dbc.Col([],width=1),
                        dbc.Col([
                            dbc.Row([
                                dbc.Progress([
                                    dbc.Progress(
                                        id=str(indicador[1][0]) + '_0-',
                                        value=indicador[1]['min_aceitavel'],
                                        color="primary",
                                        bar=True),
                                    dbc.Progress(
                                        id=str(indicador[1][0]) + '_1-',
                                        value=indicador[1]['min_esperado'] - indicador[1]['min_aceitavel'],
                                        color="warning",
                                        bar=True),
                                    dbc.Progress(
                                        id=str(indicador[1][0]) + '_2',
                                        value=indicador[1]['max_esperado'] - indicador[1]['min_esperado'],
                                        color="success",
                                        bar=True),
                                    dbc.Progress(
                                        id=str(indicador[1][0]) + '_1+',
                                        value=indicador[1]['max_aceitavel'] - indicador[1]['max_esperado'],
                                        color="warning",
                                        bar=True,
                                        striped=True),
                                    dbc.Progress(
                                        id=str(indicador[1][0]) + '_0+',
                                        value=100 - indicador[1]['max_aceitavel'],
                                        color="primary",
                                        bar=True,
                                        striped=True),
                                ], style={"height": "20px"}),
                                dbc.Tooltip(
                                    'score 0- ' + '[0 - ' + str(indicador[1]['min_aceitavel']) + ']',
                                    target=str(indicador[1][0]) + '_0-',
                                    placement='top'),
                                dbc.Tooltip(
                                    'score 1- [' + str(indicador[1]['min_aceitavel']) + ' - ' + str(indicador[1]['min_esperado']) + ']',
                                    target=str(indicador[1][0]) + '_1-',
                                    placement='top'),
                                dbc.Tooltip(
                                    'score 2 [' + str(indicador[1]['min_esperado']) + ' - ' + str(indicador[1]['max_esperado']) + ']',
                                    target=str(indicador[1][0]) + '_2',
                                    placement='top'),
                                dbc.Tooltip(
                                    'score 1+ [' + str(indicador[1]['max_esperado']) + ' - ' + str(indicador[1]['max_aceitavel']) + ']',
                                    target=str(indicador[1][0]) + '_1+',
                                    placement='top'),
                                dbc.Tooltip(
                                    'score 0+ [' + str(indicador[1]['max_aceitavel']) + ' - 100' + ']',
                                    target=str(indicador[1][0]) + '_0+',
                                    placement='top'),
                            ]),
                            html.Br(),
                            dbc.Row([
                                html.P(['intervalo aceitável: ' + str(indicador[1]['intervalo_aceitavel'])], style={'color':'orange'}),
                                html.P(['intervalo esperado: ' + str(indicador[1]['intervalo_esperado'])], style={'color':'green'}),
                            ]),
                        ], width=4),
                    ]),

                ]),
            ]),
        ],class_name="bg-light"),
        #html.Br(),
    ], fluid=True, class_name="py-3")



# Zona de introdução de texto para pesquisa
search_box = html.Div([
    dbc.Input(
        id='searchbox_indicadores',
        placeholder='search...',
        type='text',
        size='sm',
    ),
])

# Radio options para refinar a pesquisa
## ponderar adicionar mais campos de filtros, como Ativos e desactivos, Por àreas, subáreas??
radio_options=[
    {'label':'com impacto IDG','value':'com impacto IDG'},
    {'label':'sem impacto IDG','value':'sem impacto IDG'},
    {'label':'todos os indicadores','value':'todos os indicadores'},
]
radio = html.Div([
    dbc.RadioItems(
        options=radio_options,
        value='com impacto IDG',
        inline=True,
        id='radio_indicadores'
    )
])

# Barra dos filtros
filters = html.Div([
    dbc.Row([
        dbc.Col([
            search_box,
        ], width=4),
        dbc.Col([
            radio,
        ], width=8),
    ])
])

# Contagem de quantos indicadores estão selecionados
contagem = html.Div([html.P(id='contagem_indicadores')],style={'padding': '12px 0px 0px 4px'})

lista_indicadores = html.Div([],id='lista_indicadores')

# Contentor principal
container_1 = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3('indicadores'),
            html.Br(),
            filters,
            html.Br(),
            contagem,
            lista_indicadores,
        ])
    ])
], fluid=True)

# Declaração do Layout
def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])


@callback(
    Output('contagem_indicadores','children'),
    Output('lista_indicadores','children'),
    Input('searchbox_indicadores', 'value'),
    Input('radio_indicadores', 'value'),
)

def table_update(searchbox_indicadores,radio_indicadores):

    # Reset da tabela antes da pesquisa
    df_indicadores_novo = df_todos_indicadores

    # Filtragem por com impacto no IDG, sem impacto no IDG, ou todos
    ## Eventualmente pré-processar e ter os CSV's já gravados para poupar tempo
    if radio_indicadores == 'com impacto IDG':
        df_indicadores_novo = df_todos_indicadores[df_todos_indicadores['id'].isin(usf_ucsp_para_idg['indicador'].values.tolist())]
    elif radio_indicadores == 'sem impacto IDG':
        df_indicadores_novo = df_todos_indicadores[df_todos_indicadores['id'].isin(usf_ucsp_sem_idg['indicador'].values.tolist())]
    elif radio_indicadores == 'todos os indicadores':
        df_indicadores_novo = df_todos_indicadores

    # Garantir que quando a searchbox está vazia, se mostra todos os indicadores (independente dos filtros)
    if searchbox_indicadores == None or searchbox_indicadores == '':
        df_after_search = df_indicadores_novo
    else:
        search_list = process.extract(searchbox_indicadores, df_indicadores_novo.indexing, scorer=fuzz.WRatio, score_cutoff=59, limit=50)
        df_after_search = df_indicadores_novo.filter([id[2] for id in search_list], axis=0)

        # Sanity print para aferir qualidade dos resultados da pesquisa
        '''
        print(search_list)
        print(len([id[2] for id in search_list]))
        print([id[1] for id in search_list])
        '''

    # remoção das colunas que não se querem vizualizar
    df_after_search = df_after_search.drop(
        columns=[
            'codigo',
            'codigo_siars',
            'nome_abreviado',
            'formula',
            'unidade_de_medida',
            'output',
            'area_clinica',
            'tipo_de_indicador',
            'estado_do_indicador',
            'inclusao_de_utentes_no_indicador',
            'prazo_para_registos',
            'indexing',
            'nome_indicador',
        ]
    )

    #print(df_after_search.columns)

    #df_id_sdm = df_after_search.pop('id_sdm')
    #df_after_search.insert(0, 'id', df_id_sdm)

    lista_indicadores = [generate_html_indicador(i) for i in df_after_search.iterrows()]

    # Texto que refere quantos indicadores estão na tabela resultado da pesquisa
    numero_indicadores = str(len(df_after_search))+' indicadores encontrados'

    return numero_indicadores, lista_indicadores

