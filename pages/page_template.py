import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/page_template',
    title='page template',
    name='page template',
    order=5,
)

container = dbc.Container([
    dbc.Row([
        html.H3('page template'),
    ]),
    dbc.Row([
        dcc.Markdown('text')
    ]),
], fluid=True)


def layout():
    return html.Div([
        container,
        html.Br(),
    ])
