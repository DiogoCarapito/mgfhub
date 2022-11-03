import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import pandas as pd
import csv

dash.register_page(__name__,
                   path='/blog',
                   title='Blog',
                   name='Blog')

file = open('data/blog.csv','r')
blog_lines = list(csv.reader(file, delimiter=','))

'''file = open("scrapped_indicadores.csv", "r")
dados = list(csv.reader(file, delimiter=","))
df = pd.DataFrame(dados)
table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=False)

container_1 = dbc.Container([
    html.H3('blog'),
    table
    ])'''

blog = dbc.Container([
    for each in blog_lines:
        html.H3(each[0]),
        html.H3(each[1]),
])

container_1 = dbc.Container([
    html.H3('blog'),
    blog,
    ])

layout = html.Div([
    container_1,
    html.Br(),
])