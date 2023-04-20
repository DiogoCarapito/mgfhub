import base64
import io
import re

import dash
import dash_bootstrap_components as dbc
import numpy as np
import pandas as pd
from dash import html, dcc, callback, Output, Input, State

import requests


dash.register_page(
    __name__,
    path='/ct_or_mri',
    title='ct_or_mri',
    name='ct_or_mri',
    order=6

upload = html.Div([
    dcc.Upload(
        id='upload_image',
        children=html.Div([
            'Drag and Drop Image or ',
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
            html.H3('upload image'),
            dbc.Row([
                dbc.Col(width=3),
                dbc.Col([
                    upload,
                    html.Br(),
                    html.Div(id='result')
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
    Output('result', 'data'),
    Input('upload_image', 'contents'),
)

def api_request (upload_image):

    response = requests.post("https://diogocarapito-ct-or-mri-fastai.hf.space/run/predict", json={
        "data": [
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAACklEQVR4nGMAAQAABQABDQottAAAAABJRU5ErkJggg==",
        ]
    }).json()

    return response["data"]
