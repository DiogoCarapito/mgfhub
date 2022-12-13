import base64
import datetime
import io

import dash
from dash import html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc
#from dash.dependencies import Input, Output, State

from dash import dash_table
import plotly.express as px

import pandas as pd
import numpy as np
import re


dash.register_page(
    __name__,
    path='/upload',
    title='upload',
    name='upload',
    order=5,
)

upload = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Allow multiple files to be uploaded
        multiple=True
    ),
])


container_1 = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H3('upload from bi-csp'),
            dbc.Row([
                dbc.Col(width=3),
                dbc.Col([
                    upload,
                ],width=6),
                dbc.Col(width=3),
            ]),
        ])
    ]),
    dbc.Row([
        html.Div(id='output-data-upload'),
    ])
], fluid=True)

def layout():
    return html.Div([
        container_1,

        html.Br(),
        dcc.Store(id='store_data', data=[], storage_type='memory'),
    ])

def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), skiprows=2, engine='openpyxl')

            reg = '\.([0-9]*)\.'
            df_2 = pd.DataFrame([re.findall(reg, row[0]) for index, row in df.iterrows()])

            df_2.columns = ['id']
            df = df.join(df_2)

            colors_coresp = {'0-': 'red', '1-': 'yellow', '2': 'green', '1+': 'dark_yellow', '0+': 'dark_red'}
            df['color'] = [colors_coresp[row[2]] for index, row in df.iterrows()]
            df = df[[
                'id',
                'Nº Ordem',
                '\'# Métricas Indicador\'[Score V2]',
                'color',
                'Código - ID - Indicador / Médico'
            ]]
            print(df)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])



    return html.Div([
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns]
        ),
        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@callback(
    Output('output-data-upload', 'children'),

    Input('upload-data', 'contents'),
    State('upload-data', 'filename'),
    State('upload-data', 'last_modified')
)


def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children

@callback(
    Output('store_data','data'),
    Input('upload-data', 'contents'),
)

def store_data_upload(contents):
    try:
        store_data = contents.to_dict('records')
    except:
        store_data = [np.nan]

    return store_data