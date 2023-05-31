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
        html.H5('Bem-vindo ao mgfhub, uma plataforma de visualização de dados para auxiliar a gestão de cuidados de saúde primários.'),
    ]),
    html.Br(),
    html.Br(),
])

first_card = dbc.Card(
    dbc.CardBody(
        [
            html.A(
                html.H2('Indicadores'),
                href='/indicadores',
                className="card-title",
                # target='_blank'  # Open the link in a new tab
            ),
            html.Br(),
            html.P("Ferramenta de pesquisa de indicadores dos CSP sob a forma de tabla com filtros"),
            html.P("Inclui link para SDM para cada indicador"),
        ]
    )
)
second_card = dbc.Card(
    dbc.CardBody(
        [
            html.A(
                html.H2('Sunburst'),
                href='/sunburst',
                className="card-title",
                #target='_blank'  # Open the link in a new tab
            ),
            html.Br(),
            html.P("Visualização de indicadores em formato de sunburst interativo"),
            html.P("Inlcui percentagem de impacto no IDG"),
        ]
    )
)

cards = html.Div([
    dbc.Container([
        #html.H2('Ferramentas'),
        #html.Br(),
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
