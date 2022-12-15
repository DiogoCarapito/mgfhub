import base64
import io
import re

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash import html, dcc, callback, Output, Input, State



dash.register_page(
    __name__,
    path='/upload',
    title='upload',
    name='upload',
    order=5,
)

upload = html.Div([
    dcc.Upload(
        id='upload_data',
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
        multiple=False
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
                    html.Br(),
                    html.Div(id='output_data_upload')
                ],width=6),
                dbc.Col(width=3),
            ]),
        ])
    ]),
], fluid=True)

def layout():
    return html.Div([
        container_1,
        html.Br(),
    ])

@callback(
    Output('store_data', 'data'),
    Input('upload_data', 'contents'),
    State('upload_data', 'filename'),
)
def store_xlsx(contents, filename):
    try:
        content_type, content_string = contents.split(',')
        decoded = base64.b64decode(content_string)
    except:
        return np.nan
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
            df = df.rename(columns={
                '\'# Métricas Indicador\'[Score V2]': 'score',
                'Código - ID - Indicador / Médico': 'nome_indicador',
                'Nº Ordem': 'id_medico'
            })
            df = df[[
                'id',
                'id_medico',
                'score',
                'color',
                'nome_indicador'
            ]]

            df = df.assign(pontuacao=[re.findall('[0-2]', row['score']) for index, row in df.iterrows()])


    except Exception as e:
        print(e)
        return 0

    return df.to_dict('records')

@callback(
    Output('output_data_upload', 'children'),
    Input('store_data', 'data'),
)

def html_table(contents):
    if contents is None:
        return
    else:
        return html.H4(['upload sucessful'])

