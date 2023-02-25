import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/indicadores',
    title='indicadores',
    name='indicadores',
    order=0,
)

tab1_content = dbc.Card(
    dbc.CardBody([
        html.P("This is tab 1!", className="card-text"),
    ]), className="mt-3",
)

tab2_content = dbc.Card(
    dbc.CardBody([
        html.P("This is tab 2!", className="card-text"),
    ]), className="mt-3",
)


container = dbc.Container([
    html.H3('indicadores'),
    dbc.Tabs(
        [
            dbc.Tab(tab1_content, label="tabela"),
            dbc.Tab(tab2_content, label="lista"),
        ]),
], fluid=True)


def layout():
    return html.Div([
        container,
        html.Br(),
    ])

