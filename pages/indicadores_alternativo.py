import dash
from dash import html, callback, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
from unidecode import unidecode
from rapidfuzz import process, fuzz

dash.register_page(
    __name__,
    path='/indicadores_alternativo',
    title='indicadores 2',
    name='indicadores 2',
    order=3,
)

# Laod da principal base de dados em .csv
## Ponderar fazer um script para adicionar informação sobre Intervalos aceitáveis ideias a partir do PDF da Operacionalização da ACSS
## Terminar o scrapper sdm, porquen ainda falta infomração de formula de calculo
df_todos_indicadores = pd.read_csv('data/indicadores_post_processed.csv')

# Load das listas de id's de indicadores utilizados para IDG das USFs/UCSPs
## podem vir a ser adicionados a lista de indicadores doas UCC, USP, ACES
## eventualmente tem que se escrever um script para extrair diretamente do PDF da Operacionalização da ACSS
usf_ucsp_para_idg = pd.read_csv('data/usf_ucsp_indicadores_2022_comimpactoIDG.csv')
usf_ucsp_sem_idg = pd.read_csv('data/usf_ucsp_indicadores_2022_semimpactoIDG.csv')



cor_vermelha = '#CB707A'
cor_laranja = '#E6C68F'
cor_verde = '#86BF8B'

def generate_html_indicador(indicador):
    separador = ' - '
    return dbc.Container([
        dbc.Card([
            dbc.CardHeader(children=html.H5([str(indicador[1][0]) + separador + indicador[1][1]])),
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
                                        color=cor_vermelha,
                                        bar=True),
                                    dbc.Progress(
                                        id=str(indicador[1][0]) + '_1-',
                                        value=indicador[1]['min_esperado'] - indicador[1]['min_aceitavel'],
                                        color=cor_laranja,
                                        bar=True),
                                    dbc.Progress(
                                        id=str(indicador[1][0]) + '_2',
                                        value=indicador[1]['max_esperado'] - indicador[1]['min_esperado'],
                                        color=cor_verde,
                                        bar=True),
                                    dbc.Progress(
                                        id=str(indicador[1][0]) + '_1+',
                                        value=indicador[1]['max_aceitavel'] - indicador[1]['max_esperado'],
                                        color=cor_laranja,
                                        bar=True,
                                        #striped=True
                                    ),
                                    dbc.Progress(
                                        id=str(indicador[1][0]) + '_0+',
                                        value=100 - indicador[1]['max_aceitavel'],
                                        color=cor_vermelha,
                                        bar=True,
                                        #striped=True
                                    ),
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
                                html.P(['intervalo aceitável: ' + str(indicador[1]['intervalo_aceitavel'])], style={'color':cor_laranja}),
                                html.P(['intervalo esperado: ' + str(indicador[1]['intervalo_esperado'])], style={'color':cor_verde}),
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
            html.H3('cartões de indicadores'),
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

def table_update(searchbox,radio_indicadores):

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
    if searchbox == None or searchbox == '':
        df_after_search = df_indicadores_novo
    else:
        # colocar a query da search box em lowercase e remover acentos
        searchbox = unidecode(searchbox.lower())

        # fuzzy search com score cutoff de 59, comparando com indexing
        search_list = process.extract(searchbox, df_indicadores_novo['indexing'], scorer=fuzz.WRatio, score_cutoff=59, limit=50)
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

