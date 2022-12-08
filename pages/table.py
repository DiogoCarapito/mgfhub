import dash
from dash import Dash, dcc, html, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
#import plotly.graph_objects as go
from rapidfuzz import process, fuzz

dash.register_page(
    __name__,
    path='/tabela',
    title='tabela',
    name='tabela',
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
print(df_intervalos.head())

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

# Definição da Tabela
## Arranjar fomra de meter uma célula com um link para o SDM
## Alterar a font do texto da tabela, está num retro proggraming dos anos 80 xD
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
        'padding': '4px',
        'textAlign': 'left',
        'height': 'auto',
        #'minWidth': '30px', 'width': '30px','maxWidth': '360px',
        'whiteSpace': 'normal',
        'font_family': 'sans-serif',
        'font_size': '13px',
        },
    style_data={'whiteSpace': 'normal','height': 'auto',},
    style_table={'overflowX': 'auto'},
    # Linhas com fundo alternado
    style_data_conditional=[
        {
            'if': {'row_index': 'odd'},
            'backgroundColor': 'rgb(248, 248, 248)',
        }
    ],
    #export_format='xlsx',
    #export_headers='display',
)

# Zona de introdução de texto para pesquisa
search_box = html.Div([
    dbc.Input(
        id='searchbox',
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
        id='radio_tabela'
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

# Contentor principal
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

# Declaração do Layout
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

    # Reset da tabela antes da pesquisa
    df_indicadores_novo = df_todos_indicadores

    # Filtragem por com impacto no IDG, sem impacto no IDG, ou todos
    ## Eventualmente pré-processar e ter os CSV's já gravados para poupar tempo
    if radio_tabela == 'com impacto IDG':
        df_indicadores_novo = df_todos_indicadores[df_todos_indicadores['id'].isin(usf_ucsp_para_idg['indicador'].values.tolist())]
    elif radio_tabela == 'sem impacto IDG':
        df_indicadores_novo = df_todos_indicadores[df_todos_indicadores['id'].isin(usf_ucsp_sem_idg['indicador'].values.tolist())]
    elif radio_tabela == 'todos os indicadores':
        df_indicadores_novo = df_todos_indicadores

    # Garantir que quando a searchbox está vazia, se mostra todos os indicadores (independente dos filtros)
    if searchbox == None or searchbox == '':
        df_after_search = df_indicadores_novo
    else:
        search_list = process.extract(searchbox, df_indicadores_novo.indexing, scorer=fuzz.WRatio, score_cutoff=59, limit=50)
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
            'id',
            'codigo',
            'codigo_siars',
            'nome_abreviado',
            'formula',
            'unidade_de_medida',
            'output',
            'tipo_de_indicador',
            'estado_do_indicador',
            'inclusao_de_utentes_no_indicador',
            'prazo_para_registos',
            'link',
            'indexing'
        ]
    )


    df_id_sdm = df_after_search.pop('id_sdm')
    df_after_search.insert(0, 'id', df_id_sdm)

    # Duas variáveis necessárias à exportação da tabela
    df_data = df_after_search.to_dict(orient='records')
    df_columns = [{'id': x, 'name': x, 'presentation': 'markdown'} if x == 'id' else {'id': x, 'name': x} for x in df_after_search.columns]
    #df_columns = [{"name": i, "id": i} for i in df_after_search.columns]

    # Texto que refere quantos indicadores estão na tabela resultado da pesquisa
    numero_indicadores = str(len(df_after_search))+' indicadores encontrados'

    return df_data,df_columns,numero_indicadores

