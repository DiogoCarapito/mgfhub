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
posts_html = str()
blogposts = [['first post','4/11/2022','text text'],['second post','8/11/2022','text text2']]
for each in blogposts:
    post = html.Div(dbc.Container([
                html.H2(each[0]),
                html.P(each[1]),
                html.Hr(className="my-2"),
                html.P(each[2]),
            ],fluid=True, className="py-3",
        ),className="p-3 bg-light rounded-3",
    ),

'''
jumbotron = html.Div(
    dbc.Container(
        [
            html.H2(blogposts[0][0]),
            html.P(blogposts[0][1]),
            html.Hr(className="my-2"),
            html.P(blogposts[0][2]),
        ],fluid=True, className="py-3",
    ),className="p-3 bg-light rounded-3",
)
'''

blog = dbc.Container([
    html.H3('blog'),
], fluid=True,)

container_1 = dbc.Container([
    html.H3('blog'),
    blog,
    ], fluid=True,)


def layout():
    return html.Div([
        posts_html,
        html.Br(),
    ])
