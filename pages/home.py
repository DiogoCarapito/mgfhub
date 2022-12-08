import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/',
    title='bi indicadires',
    name='bi indicadores',
    order=1,
)

card_1 = dbc.Card(
    [
        dbc.CardImg(src="data/table_image.png", top=True),
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "18rem"},
)

card_2 = dbc.Card(
    [
        dbc.CardImg(src="sunburst_image.png", top=True),
        dbc.CardBody(
            [
                html.H4("Card title", className="card-title"),
                html.P(
                    "Some quick example text to build on the card title and "
                    "make up the bulk of the card's content.",
                    className="card-text",
                ),
                dbc.Button("Go somewhere", color="primary"),
            ]
        ),
    ],
    style={"width": "18rem"},
)


container_1 = dbc.Container([
    html.Br(),
    dbc.Row([
        dbc.Col([
            card_1
        ],width = 6),
        dbc.Col([
            card_2
        ],width = 6),
    ]),
], fluid=True)

def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])
