import dash
from dash import dcc, html
#import dash_core_components as dcc
#import dash_html_components as html

# for deployment, pass app.server (which is the actual flask app) to WSGI etc
app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children='HELLO YOLO WORLD'),

    html.Div(children='''
        HELLO YOLO WORLD
    '''),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])

if __name__ == "__main__":
    app.run(debug=True)