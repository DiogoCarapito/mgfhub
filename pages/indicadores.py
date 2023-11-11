import dash
from dash import html, callback, Input, Output, dash_table
import dash_bootstrap_components as dbc
import pandas as pd
from unidecode import unidecode
from rapidfuzz import process, fuzz
import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# import time

dash.register_page(
    __name__,
    path="/indicadores",
    title="indicadores",
    name="indicadores",
    order=2,
)
load_dotenv()
# Supabase configuration
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


def supabase_insert(input_text):
    # Get current datetime
    date_time = datetime.now().isoformat()
    # Create the data in a format to be inserted into Supabase
    sb_insert = {"created_at": date_time, "query": input_text}
    # Insert data into Supabase
    supabase.table("mgfhub_queries").insert(sb_insert).execute()


# definir cores
cor_vermelha = "#CB707A"
cor_laranja = "#E6C68F"
cor_verde = "#86BF8B"

# Laod da principal base de dados em .csv
## Ponderar fazer um script para adicionar informação sobre Intervalos aceitáveis ideias a partir do PDF da Operacionalização da ACSS
## Terminar o scrapper sdm, porquen ainda falta infomração de formula de calculo
df_todos_indicadores = pd.read_csv("data/indicadores_post_processed.csv")

# Load das listas de id's de indicadores utilizados para IDG das USFs/UCSPs
## podem vir a ser adicionados a lista de indicadores doas UCC, USP, ACES
## eventualmente tem que se escrever um script para extrair diretamente do PDF da Operacionalização da ACSS
usf_ucsp_para_idg = pd.read_csv("data/usf_ucsp_indicadores_2022_comimpactoIDG.csv")
usf_ucsp_sem_idg = pd.read_csv("data/usf_ucsp_indicadores_2022_semimpactoIDG.csv")


# definição de cartão
def generate_html_indicador(indicador):
    separador = " - "
    return dbc.Container(
        [
            dbc.Card(
                [
                    dbc.CardHeader(
                        children=html.H5(
                            [str(indicador[1][0]) + separador + indicador[1][1]]
                        )
                    ),
                    dbc.CardBody(
                        [
                            dbc.Container(
                                [
                                    dbc.Row(
                                        [
                                            dbc.Col(
                                                [
                                                    dbc.Row(
                                                        [
                                                            html.B(
                                                                [
                                                                    str(
                                                                        indicador[1][
                                                                            "area"
                                                                        ]
                                                                    )
                                                                    + " > "
                                                                    + str(
                                                                        indicador[1][
                                                                            "subarea"
                                                                        ]
                                                                    )
                                                                    + " > "
                                                                    + str(
                                                                        indicador[1][
                                                                            "dimensao"
                                                                        ]
                                                                    )
                                                                ]
                                                            )
                                                        ]
                                                    ),
                                                    html.Br(),
                                                    dbc.Row(
                                                        [
                                                            html.P(
                                                                [
                                                                    indicador[1][
                                                                        "objetivo"
                                                                    ]
                                                                ]
                                                            ),
                                                            html.A(
                                                                indicador[1]["link"],
                                                                href=indicador[1][
                                                                    "link"
                                                                ],
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                                width=7,
                                            ),
                                            dbc.Col([], width=1),
                                            dbc.Col(
                                                [
                                                    dbc.Row(
                                                        [
                                                            dbc.Progress(
                                                                [
                                                                    dbc.Progress(
                                                                        id=str(
                                                                            indicador[
                                                                                1
                                                                            ][0]
                                                                        )
                                                                        + "_0-",
                                                                        value=indicador[
                                                                            1
                                                                        ][
                                                                            "min_aceitavel"
                                                                        ],
                                                                        color=cor_vermelha,
                                                                        bar=True,
                                                                    ),
                                                                    dbc.Progress(
                                                                        id=str(
                                                                            indicador[
                                                                                1
                                                                            ][0]
                                                                        )
                                                                        + "_1-",
                                                                        value=indicador[
                                                                            1
                                                                        ][
                                                                            "min_esperado"
                                                                        ]
                                                                        - indicador[1][
                                                                            "min_aceitavel"
                                                                        ],
                                                                        color=cor_laranja,
                                                                        bar=True,
                                                                    ),
                                                                    dbc.Progress(
                                                                        id=str(
                                                                            indicador[
                                                                                1
                                                                            ][0]
                                                                        )
                                                                        + "_2",
                                                                        value=indicador[
                                                                            1
                                                                        ][
                                                                            "max_esperado"
                                                                        ]
                                                                        - indicador[1][
                                                                            "min_esperado"
                                                                        ],
                                                                        color=cor_verde,
                                                                        bar=True,
                                                                    ),
                                                                    dbc.Progress(
                                                                        id=str(
                                                                            indicador[
                                                                                1
                                                                            ][0]
                                                                        )
                                                                        + "_1+",
                                                                        value=indicador[
                                                                            1
                                                                        ][
                                                                            "max_aceitavel"
                                                                        ]
                                                                        - indicador[1][
                                                                            "max_esperado"
                                                                        ],
                                                                        color=cor_laranja,
                                                                        bar=True,
                                                                        # striped=True
                                                                    ),
                                                                    dbc.Progress(
                                                                        id=str(
                                                                            indicador[
                                                                                1
                                                                            ][0]
                                                                        )
                                                                        + "_0+",
                                                                        value=100
                                                                        - indicador[1][
                                                                            "max_aceitavel"
                                                                        ],
                                                                        color=cor_vermelha,
                                                                        bar=True,
                                                                        # striped=True
                                                                    ),
                                                                ],
                                                                style={
                                                                    "height": "20px"
                                                                },
                                                            ),
                                                            dbc.Tooltip(
                                                                "score 0- "
                                                                + "[0 - "
                                                                + str(
                                                                    indicador[1][
                                                                        "min_aceitavel"
                                                                    ]
                                                                )
                                                                + "]",
                                                                target=str(
                                                                    indicador[1][0]
                                                                )
                                                                + "_0-",
                                                                placement="top",
                                                            ),
                                                            dbc.Tooltip(
                                                                "score 1- ["
                                                                + str(
                                                                    indicador[1][
                                                                        "min_aceitavel"
                                                                    ]
                                                                )
                                                                + " - "
                                                                + str(
                                                                    indicador[1][
                                                                        "min_esperado"
                                                                    ]
                                                                )
                                                                + "]",
                                                                target=str(
                                                                    indicador[1][0]
                                                                )
                                                                + "_1-",
                                                                placement="top",
                                                            ),
                                                            dbc.Tooltip(
                                                                "score 2 ["
                                                                + str(
                                                                    indicador[1][
                                                                        "min_esperado"
                                                                    ]
                                                                )
                                                                + " - "
                                                                + str(
                                                                    indicador[1][
                                                                        "max_esperado"
                                                                    ]
                                                                )
                                                                + "]",
                                                                target=str(
                                                                    indicador[1][0]
                                                                )
                                                                + "_2",
                                                                placement="top",
                                                            ),
                                                            dbc.Tooltip(
                                                                "score 1+ ["
                                                                + str(
                                                                    indicador[1][
                                                                        "max_esperado"
                                                                    ]
                                                                )
                                                                + " - "
                                                                + str(
                                                                    indicador[1][
                                                                        "max_aceitavel"
                                                                    ]
                                                                )
                                                                + "]",
                                                                target=str(
                                                                    indicador[1][0]
                                                                )
                                                                + "_1+",
                                                                placement="top",
                                                            ),
                                                            dbc.Tooltip(
                                                                "score 0+ ["
                                                                + str(
                                                                    indicador[1][
                                                                        "max_aceitavel"
                                                                    ]
                                                                )
                                                                + " - 100"
                                                                + "]",
                                                                target=str(
                                                                    indicador[1][0]
                                                                )
                                                                + "_0+",
                                                                placement="top",
                                                            ),
                                                        ]
                                                    ),
                                                    html.Br(),
                                                    dbc.Row(
                                                        [
                                                            html.P(
                                                                [
                                                                    "intervalo aceitável: "
                                                                    + str(
                                                                        indicador[1][
                                                                            "intervalo_aceitavel"
                                                                        ]
                                                                    )
                                                                ],
                                                                style={
                                                                    "color": cor_laranja
                                                                },
                                                            ),
                                                            html.P(
                                                                [
                                                                    "intervalo esperado: "
                                                                    + str(
                                                                        indicador[1][
                                                                            "intervalo_esperado"
                                                                        ]
                                                                    )
                                                                ],
                                                                style={
                                                                    "color": cor_verde
                                                                },
                                                            ),
                                                        ]
                                                    ),
                                                ],
                                                width=4,
                                            ),
                                        ]
                                    ),
                                ]
                            ),
                        ]
                    ),
                ],
                class_name="bg-light",
            ),
            # html.Br(),
        ],
        fluid=True,
        class_name="py-3",
    )


# Definição da Tabela
## Arranjar fomra de meter uma célula com um link para o SDM
## Alterar a font do texto da tabela, está num retro proggraming dos anos 80 xD
table = dash_table.DataTable(
    id="tabela_indicadores",
    page_size=25,
    sort_action="native",
    # filter_action='native',
    style_header={"backgroundColor": "rgb(240, 240, 240)", "fontWeight": "bold"},
    style_cell={
        "padding": "4px",
        "textAlign": "left",
        "height": "auto",
        #'minWidth': '30px', 'width': '30px','maxWidth': '360px',
        "whiteSpace": "normal",
        "font_family": "sans-serif",
        "font_size": "13px",
        # permitir que texto possa ser selecionado
        "user-select": "text",
    },
    style_data={
        "whiteSpace": "normal",
        "height": "auto",
    },
    style_table={"overflowX": "auto"},
    editable=True,
    # Linhas com fundo alternado
    style_data_conditional=[
        {
            "if": {"row_index": "odd"},
            "backgroundColor": "rgb(248, 248, 248)",
        }
    ],
    # export_format='xlsx',
    # export_headers='display',
)

# Zona de introdução de texto para pesquisa
search_box = html.Div(
    [
        dbc.Input(
            id="searchbox",
            placeholder="procurar...",
            type="text",
            size="sm",
        ),
    ]
)

# Radio options para refinar a pesquisa
## ponderar adicionar mais campos de filtros, como Ativos e desactivos, Por àreas, subáreas??
radio_options = [
    {"label": "com impacto IDG", "value": "com impacto IDG"},
    {"label": "sem impacto IDG", "value": "sem impacto IDG"},
    {"label": "todos os indicadores", "value": "todos os indicadores"},
]
radio = html.Div(
    [
        dbc.RadioItems(
            options=radio_options,
            value="com impacto IDG",
            inline=True,
            id="radio_tabela",
        )
    ]
)

# Barra dos filtros
filters = html.Div(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        search_box,
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        radio,
                    ],
                    width=8,
                ),
            ]
        )
    ]
)

# Contagem de quantos indicadores estão selecionados
contagem = html.Div(
    [html.P(id="searchbox_indicadores_tabela")], style={"padding": "12px 0px 0px 4px"}
)

cartoes_indicadores = html.Div([], id="cartoes_indicadores")

tab1_tabela = dbc.Card(dbc.CardBody([table], className="p-0"))
# ,style={"background-color": "#ADD8E6"}
tab2_cartões = dbc.Card(
    dbc.CardBody([cartoes_indicadores], className="p-0"),
)

tabs = dbc.Tabs(
    [
        dbc.Tab(tab1_tabela, label="tabela"),
        dbc.Tab(tab2_cartões, label="cartões"),
    ]
)

# Contentor principal
container_1 = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        html.H3("indicadores"),
                        html.Br(),
                        filters,
                        contagem,
                        tabs,
                    ]
                )
            ]
        )
    ],
    fluid=True,
)


# Declaração do Layout
def layout():
    return html.Div(
        [
            container_1,
            html.Br(),
        ]
    )


@callback(
    Output("tabela_indicadores", "data"),
    Output("tabela_indicadores", "columns"),
    Output("cartoes_indicadores", "children"),
    Output("searchbox_indicadores_tabela", "children"),
    Input("searchbox", "value"),
    Input("radio_tabela", "value"),
)
def table_update(searchbox, radio_tabela):
    # Reset da tabela antes da pesquisa
    df_indicadores_novo = df_todos_indicadores

    # Filtragem por com impacto no IDG, sem impacto no IDG, ou todos
    ## Eventualmente pré-processar e ter os CSV's já gravados para poupar tempo
    if radio_tabela == "com impacto IDG":
        df_indicadores_novo = df_todos_indicadores[
            df_todos_indicadores["id"].isin(
                usf_ucsp_para_idg["indicador"].values.tolist()
            )
        ]
    elif radio_tabela == "sem impacto IDG":
        df_indicadores_novo = df_todos_indicadores[
            df_todos_indicadores["id"].isin(
                usf_ucsp_sem_idg["indicador"].values.tolist()
            )
        ]
    elif radio_tabela == "todos os indicadores":
        df_indicadores_novo = df_todos_indicadores

    # Garantir que quando a searchbox está vazia, se mostra todos os indicadores (independente dos filtros)
    if searchbox == None or searchbox == "":
        df_after_search = df_indicadores_novo
    else:
        # colocar a query da search box em lowercase e remover acentos
        searchbox = unidecode(searchbox.lower())

        # fuzzy search com score cutoff de 59, comparando com indexing
        search_list = process.extract(
            searchbox,
            df_indicadores_novo["indexing"],
            scorer=fuzz.WRatio,
            score_cutoff=59,
            limit=50,
        )
        df_after_search = df_indicadores_novo.filter(
            [id[2] for id in search_list], axis=0
        )

    # remoção das colunas que não se querem vizualizar
    df_after_search_tabela = df_after_search.copy()

    df_after_search_tabela = df_after_search_tabela.drop(
        columns=[
            "id",
            "codigo",
            "codigo_siars",
            "nome_abreviado",
            "objetivo",
            "formula",
            "unidade_de_medida",
            "output",
            "area_clinica",
            "tipo_de_indicador",
            "estado_do_indicador",
            "inclusao_de_utentes_no_indicador",
            "prazo_para_registos",
            "link",
            "indexing",
            "nome_indicador",
            "min_aceitavel",
            "min_esperado",
            "max_esperado",
            "max_aceitavel",
        ]
    )

    df_id_sdm = df_after_search_tabela.pop("id_sdm")
    df_after_search_tabela.insert(0, "id", df_id_sdm)

    # Duas variáveis necessárias à exportação da tabela
    df_data = df_after_search_tabela.to_dict(orient="records")
    df_columns = [
        {"id": x, "name": x, "presentation": "markdown"}
        if x == "id"
        else {"id": x, "name": x}
        for x in df_after_search_tabela.columns
    ]
    # df_columns = [{"name": i, "id": i} for i in df_after_search.columns]

    df_after_search_cartoes = df_after_search.copy()

    df_after_search_cartoes = df_after_search_cartoes.drop(
        columns=[
            "codigo",
            "codigo_siars",
            "nome_abreviado",
            "formula",
            "unidade_de_medida",
            "output",
            "area_clinica",
            "tipo_de_indicador",
            "estado_do_indicador",
            "inclusao_de_utentes_no_indicador",
            "prazo_para_registos",
            "indexing",
            "nome_indicador",
        ]
    )

    cartoes_indicadores_gerados = [
        generate_html_indicador(i) for i in df_after_search_cartoes.iterrows()
    ]

    # Texto que refere quantos indicadores estão na tabela resultado da pesquisa
    numero_indicadores_tabela = str(len(df_after_search)) + " indicadores encontrados"

    if searchbox == None or searchbox == "":
        pass
    # se for text com mais de 2 caracteres, ou se for um  numero, inserir na base de dados supabase
    elif len(searchbox) > 2 or searchbox.isnumeric():
        supabase_insert(searchbox)
    else:
        pass

    return (
        df_data,
        df_columns,
        cartoes_indicadores_gerados,
        numero_indicadores_tabela,
    )
