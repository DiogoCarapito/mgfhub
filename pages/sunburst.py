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
    order=2,
)

pythonanywhere_file_tree = ''
#pythonanywhere_file_tree = '/home/diogocarapito/bi_indicadores/'

df_todos_indicadores = pd.read_csv(pythonanywhere_file_tree + 'data/scrapped_indicadores.csv')
usf_ucsp_para_idg = pd.read_csv(pythonanywhere_file_tree + 'data/usf_ucsp_indicadores_2022_comimpactoIDG.csv')
df_todos_indicadores_filtrado = df_todos_indicadores[df_todos_indicadores['id'].isin(usf_ucsp_para_idg['indicador'].values.tolist())]
df = df_todos_indicadores_filtrado.drop(columns=['codigo','codigo_siars','objetivo','formula','unidade_de_medida', 'output','estado_do_indicador','tipo_de_indicador','area_clinica','inclusao_de_utentes_no_indicador','prazo_para_registos','link'])

df_area = pd.DataFrame({
    'id':df.area.drop_duplicates(),
    'label':df.area.drop_duplicates(),
    'parent':[np.nan for each in df.area.drop_duplicates()],
    'value':[50,10,20,10]
})
df_area_2 = pd.DataFrame({
    'id': ['Atividade Científica'],
    'label': ['Atividade Científica'],
    'parent':[np.nan],
    'value':[10],
})
df_area = pd.concat([df_area,df_area_2])

df_subarea = pd.DataFrame({
    'id':df.subarea.drop_duplicates(),
    'label':df.subarea.drop_duplicates(),
    'parent':[df.loc[each]['area'] for each in df.subarea.drop_duplicates().index],
    'value':[10,10,10,10,8,2,8,8,8,4]
})
df_subarea_2 = pd.DataFrame({
    'id':[
        'Satisfação de Utentes',
        'Formação Externa',
        'Autoria de Artigos Escritos',
        'Trabalhos de Investigação'],
    'label':[
        'Satisfação de Utentes',
        'Formação Externa',
        'Autoria de Artigos Escritos',
        'Trabalhos de Investigação'],
    'parent':[
        'Desempenho',
        'Formação',
        'Atividade Científica',
        'Atividade Científica'],
    'value':[
        10,
        2,
        5,
        5],
})
df_subarea = pd.concat([df_subarea,df_subarea_2])

df_dimensao = pd.DataFrame({
    'id':df.dimensao.drop_duplicates(),
    'label':df.dimensao.drop_duplicates(),
    'parent':[df.loc[each]['subarea'] for each in df.dimensao.drop_duplicates().index],
    'value':[
        1, #Personalização
        1, #Cobertura ou Utilização
        2.5, #Saúde da Mulher
        2.5, #Hipertensão Arterial
        2.5, #Saúde do Idoso
        2.5, #Saúde do Adulto
        2.5, #Diabetes Mellitus
        2.5, #Doenças Aparelho Respiratório
        2.5, #Saúde Infantil e Juvenil
        5, #Prescrição Farmacoterapêutica
        3, #Prescrição MCDT
        4, #Tempos Máximos de Resposta Garantidos Acesso
        1, #Consulta no Próprio Dia
        1, #Distribuição das Consultas Presenciais no Dia
        2.5, #Multimorbilidade e Outros Tipos de Doenças
        8, #Serviços Assistenciais
        1.6, #Governação Clínica
        2, #Acesso
        6, #Prog. Melh. Contínua Qual. e Proc. Assist. Int...
        4, #Formação da Equipa Multiprofissional
        4, #Formação de Internos e Alunos
        3.2, #Segurança de Utentes
        4, #Participação do Cidadão
    ]
})

df_dimensao = df_dimensao.drop(index=[378,376])
df_dimensao_2 = pd.DataFrame({
        'id':['Serviços de Carácter Assistencial','Acesso MCQ'],
        'label':['Serviços de Carácter Assistencial','Acesso MCQ'],
        'parent':['Serviços Assistenciais','Melhoria Contínua'],
        'value':[8,2]},
    index=[376,378])
df_dimensao_3 = pd.DataFrame({
        'id':[
            'Atendimento Telefónico',
            'Trajeto do Utente na Unidade Funcional',
            'Prescrição de Cuidados',
            'Outras Atividades não Assistenciais',
            'Segurança de Profissionais',
            'Gestão do Risco',
        ],
        'label':[
            'Atendimento Telefónico',
            'Trajeto do Utente na Unidade Funcional',
            'Prescrição de Cuidados',
            'Outras Atividades não Assistenciais',
            'Segurança de Profissionais',
            'Gestão do Risco',
        ],
        'parent':[
            'Acesso',
            'Acesso',
            'Qualificação da Prescrição',
            'Serviços não Assistenciais',
            'Segurança',
            'Segurança',
        ],
        'value':[
            1,
            1,
            2,
            0.4,
            2.4,
            2.4
        ]},
    index=[0,0,0,0,0,0])
df_dimensao = pd.concat([df_dimensao,df_dimensao_2,df_dimensao_3])

df_indicadores = pd.DataFrame({
    'id':df.nome_abreviado.drop_duplicates(),
    'label':df.nome_abreviado.drop_duplicates(),
    'parent':[df.loc[each]['dimensao'] for each in df.nome_abreviado.drop_duplicates().index],
})

df_sunburst = pd.concat([df_area,df_subarea,df_dimensao,df_indicadores])
df_sunburst_2 = pd.concat([df_area,df_subarea,df_dimensao])

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


header = dbc.Container((
    dbc.Row([
        html.H3('sunburst'),
    ]),
))

container = dbc.Container([
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sunburst_indicadores')
        ], width=6),
        dbc.Col([
            dcc.Graph(id='sunburst_indicadores_2')
        ], width=6),
    ]),
], fluid=True)


def layout():
    return html.Div([
        header,
        filters,
        html.Br(),
        container,
        html.Br(),
    ])


@callback(
    Output('sunburst_indicadores', 'figure'),
    Output('sunburst_indicadores_2', 'figure'),
    #Output('sunburst', 'figure'),
    Input('radio_tabela', 'value'),
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

    fig_sunburst_indicadores = go.Figure()
    fig_sunburst_indicadores.add_trace(go.Sunburst(
        ids=df_sunburst.id,
        labels=df_sunburst.label,
        parents=df_sunburst.parent,
        #values=df_sunburst.value,
        branchvalues="total",
        #domain=dict(column=1),
        insidetextorientation='radial',
    ))
    fig_sunburst_indicadores.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    fig_sunburst_indicadores_2 = go.Figure()
    fig_sunburst_indicadores_2.add_trace(go.Sunburst(
        ids=df_sunburst_2.id,
        labels=df_sunburst_2.label,
        parents=df_sunburst_2.parent,
        values=df_sunburst_2.value,
        branchvalues="total",
        # domain=dict(column=1),
        insidetextorientation='radial',
    ))
    fig_sunburst_indicadores_2.update_layout(margin=dict(t=0, l=0, r=0, b=0))

    '''
    df_coffe = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/718417069ead87650b90472464c7565dc8c2cb1c/coffee-flavors.csv')
    fig = go.Figure()
    fig.add_trace(go.Sunburst(
        ids=df_coffe.ids,
        labels=df_coffe.labels,
        parents=df_coffe.parents,
        domain=dict(column=1),
        maxdepth=2,
        insidetextorientation='radial'
    ))
    fig.update_layout(
        margin=dict(t=10, l=10, r=10, b=10)
    )
    '''

    return fig_sunburst_indicadores,fig_sunburst_indicadores_2
