import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

dash.register_page(
    __name__,
    path='/blog',
    title='blog',
    name='blog',
    order=4,
)

pythonanywhere_file_tree = ''
#pythonanywhere_file_tree = '/home/diogocarapito/bi_indicadores/'

blog_posts_html = []
blogposts = pd.read_csv(pythonanywhere_file_tree + 'data/blog.csv')

'''
for post,item in blogposts.iterrows():
    #html = html.Div([dbc.Container([html.H2(item['title']),])])
    #blog_posts_html.append(html)
    print(item['title'])

'''

'''
for each in blogposts:
    post = html.Div(
        dbc.Container([
                    html.H2(each[0]),
                    html.P(each[1]),
                    html.Hr(className="my-2"),
                    html.P(each[2]),
                ],fluid=True, className="py-3",
            ),className="p-3 bg-light rounded-3",
        )
    blog_posts_html.append(post)
'''

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

container_1 = dbc.Container([
    html.H3('blog'),
    html.Div(blog_posts_html),
    ], fluid=True,)


def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])
