import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/blog',
    title='blog',
    name='blog',
    order=2,
)

blog = dbc.Container([
    html.H3('blog'),
], fluid=True,)

container_1 = dbc.Container([
    html.H3('blog'),
    blog,
    ], fluid=True,)


def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])
