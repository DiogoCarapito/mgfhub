import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/',
    title='home',
    name='home',
    order=1,
)

card_1 = dbc.Card([
    dbc.CardBody([
        html.H4("tabela", className="card-title"),
        html.P("pesquisar e explorar os diferentes indicadores em forma de tabela.",className="card-text",),
        dbc.Button("tabela", color="info",href='/tabela'),
    ]),
])

card_2 = dbc.Card([
    dbc.CardBody([
        html.H4("sunburst", className="card-title"),
        html.P("navegar pelos indicadores em visualização interactiva",className="card-text"),
        dbc.Button("sunburst", color="info", href='/sunburst'),
    ])
])



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
