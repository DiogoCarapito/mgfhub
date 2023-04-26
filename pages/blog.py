import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(
    __name__,
    path='/blog',
    title='blog',
    name='blog',
    order=5,
)

pythonanywhere_file_tree = ''
#pythonanywhere_file_tree = '/home/diogocarapito/bi_indicadores/'

blog_posts_html = []
blogposts = pd.read_csv(pythonanywhere_file_tree + 'data/blog.csv')

def generate_blog_post(blogpost):
    return dbc.Container([
        html.H3(blogpost[1][0]),
        html.H5(blogpost[1][1]),
        html.P(blogpost[1][2]),
        html.A([blogpost[1][3]],href=blogpost[1][3]),
        html.Hr(className="my-2"),
        html.Br(),
        ],fluid=True, className="py-3")

container = dbc.Container([
    html.H1('blog'),
    html.Br(),
    html.Div(children=[generate_blog_post(i) for i in blogposts.iterrows()]),
    ], fluid=True,)


def layout():
    return html.Div([
        container,
        html.Br(),
    ])
