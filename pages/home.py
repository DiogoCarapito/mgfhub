import dash
from dash import html
import dash_bootstrap_components as dbc

# from dash import dcc

dash.register_page(
    __name__,
    path="/",
    title="",
    name="",
    order=1,
)

introduction = html.Div(
    [
        dbc.Container(
            [
                html.H1("mgfhub", style={"text-align": "center"}),
                html.Br(),
                html.P(
                    "Uma plataforma de pesquisa e visualização de indicadores para auxiliar a gestão de cuidados de saúde primários.",
                    style={"text-align": "center"},
                ),
            ]
        ),
        html.Br(),
        html.Br(),
    ]
)

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.A(
                html.H2("Indicadores"),
                href="/indicadores",
                className="card-title",
                style={"display": "flex", "justify-content": "center", "color": "blue"},
                # target='_blank'  # Open the link in a new tab
            ),
            html.Br(),
            html.Div(
                [
                    html.Img(src="/assets/tabela.jpg", style={"width": "80%"}),
                ],
                style={"display": "flex", "justify-content": "center"},
            ),
            html.Br(),
            html.Br(),
            html.P(
                "Ferramenta de pesquisa de indicadores dos CSP sob a forma de tabla com filtros"
            ),
            html.P("Inclui link para SDM para cada indicador"),
        ]
    ),
    style={
        "width": "80%",  # Set the card width to 80% of the parent container
        "max-width": "600px",  # Set a maximum width to limit card expansion on larger screens
        "margin": "auto",  # Center the card horizontally within the parent container
    },
)
second_card = dbc.Card(
    dbc.CardBody(
        [
            html.A(
                html.H2("Sunburst"),
                href="/sunburst",
                className="card-title",
                style={"display": "flex", "justify-content": "center", "color": "blue"},
                # target='_blank'  # Open the link in a new tab
            ),
            html.Br(),
            html.Div(
                [
                    html.Img(src="/assets/sunburst.jpg", style={"width": "50%"}),
                ],
                style={"display": "flex", "justify-content": "center"},
            ),
            html.Br(),
            html.Br(),
            html.P("Visualização de indicadores em formato de sunburst interativo"),
            html.P("Inlcui percentagem de impacto no IDG"),
        ]
    ),
    style={
        "width": "80%",  # Set the card width to 80% of the parent container
        "max-width": "600px",  # Set a maximum width to limit card expansion on larger screens
        "margin": "auto",  # Center the card horizontally within the parent container
    },
)

cards = html.Div(
    [
        dbc.Container(
            [
                html.Div(
                    style={"display": "flex", "justify-content": "center"},
                    children=[first_card],
                ),
                html.Br(),
                html.Div(
                    style={"display": "flex", "justify-content": "center"},
                    children=[second_card],
                ),
            ]
        ),
    ],
    style={"display": "flex", "justify-content": "center"},
)


main_page_layout = dbc.Container(
    [
        introduction,
        html.Br(),
        cards,
    ],
    fluid=True,
)


def layout():
    return html.Div(
        [
            main_page_layout,
        ]
    )
