import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import csv

dash.register_page(
    __name__,
    path='/blog',
    title='blog',
    name='blog',
    order=2,
)

#file = open('/data/blog.csv','r')
#blog_lines = list(csv.reader(file, delimiter=','))

'''file = open("scrapped_indicadores.csv", "r")
dados = list(csv.reader(file, delimiter=","))
df = pd.DataFrame(dados)
table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=False)

container_1 = dbc.Container([
    html.H3('blog'),
    table
    ])'''

blog = dbc.Container([
    html.H3('blog'),
],fluid=True,)

container_1 = dbc.Container([
    html.H3('blog'),
    blog,
    ],fluid=True,)

def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])