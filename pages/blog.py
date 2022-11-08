import dash
from dash import html
import dash_bootstrap_components as dbc

dash.register_page(
    __name__,
    path='/blog',
    title='blog',
    name='blog',
    order=4,
)

blogposts = [['4/11/2022','first post','text text'],[]]

jumbotron = html.Div(
    dbc.Container(
        [
            html.H4("Jumbotron", className="display-3"),
            html.P(
                "Use Containers to create a jumbotron to call attention to "
                "featured content or information.",
                className="lead",
            ),
            html.Hr(className="my-2"),
            html.P(
                "Use utility classes for typography and spacing to suit the "
                "larger container."
            ),
        ],
        fluid=True,
        className="py-3",
    ),
    className="p-3 bg-light rounded-3",
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
        jumbotron,
        html.Br(),
    ])
