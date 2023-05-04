import dash
from dash import html
import dash_bootstrap_components as dbc
from dash import dcc

dash.register_page(
    __name__,
    path='/',
    title='',
    name='',
    order=1,
)



introduction = html.Div([
    dbc.Container([
        html.H1('mgfhub'),
        html.Br(),
        html.P('Bem-vindo ao mgfhub, uma plataforma de visualização de dados para auxiliar a gestão de cuidados de saúde primários.'),
    ]),
    html.Br(),
    html.Br(),
])

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3("indicadores", className="card-title"),
            html.Br(),
            html.P("Ferramenta de pesquisa de indicadores dos CSP"),
            html.P("Inclui link para SDM"),
            dbc.Button("Link", color="info", href='/indicadores'),
        ]
    )
)
second_card = dbc.Card(
    dbc.CardBody(
        [
            html.H3("sunburst", className="card-title"),
            html.Br(),
            html.P("Visualização de indicadores em formato de sunburst."),
            html.P("Inlcui percentagem de impacto no IDG"),
            dbc.Button("Link", color="info", href='/sunburst'),
        ]
    )
)

cards = html.Div([
    dbc.Container([
        html.H1('ferramentas'),
        html.Br(),
        dbc.Row([
            dbc.Col(first_card, width=6),
            dbc.Col(second_card, width=6),
        ]),
    ]),
])
container = dbc.Container([
    introduction,
    html.Br(),
    cards,
], fluid=True)

def layout():
    return html.Div([
        container,
    ])
