import dash
from dash import html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go


dash.register_page(
    __name__,
    path='/sunburst',
    title='sunburst',
    name='sunburst',
    order=3,
)

pythonanywhere_file_tree = ''
#pythonanywhere_file_tree = '/home/diogocarapito/bi_indicadores/'
df_sunburst = pd.read_csv(pythonanywhere_file_tree + 'data/sunburst_data.csv')

dropdown_options = ['unidade']

filters = html.Div([
    dbc.Row([
        dbc.Col([],width=4),
        dbc.Col([
            dcc.Dropdown(
                options=dropdown_options,
                value=dropdown_options[0],
                id='dropdown_options'
            )
        ],width=4),
        dbc.Col([],width=4),
    ])
])


header = html.Div((
    dbc.Row([
        html.H3('sunburst'),
    ]),
))

graphs = html.Div([
    dbc.Row([
        dbc.Col([],width=1),
        dbc.Col([
            dcc.Graph(id='sunburstindicadores')
        ], width=10),
        dbc.Col([], width=1),
    ]),

])

container = dbc.Container([
    dbc.Row([
        dbc.Col([
            header,
            filters,
            html.Br(),
            graphs,
            html.Br(),
            html.Div(id='test_container'),
        ])
    ])
], fluid=True)


def layout():
    return html.Div([
        container,
        html.Br(),
    ])


@callback(
    Output('dropdown_options', 'options'),
    Input('store_data', 'data'),
)

def stora_data_show(store_data):

    if store_data == []:
        return []
    else:
        df=pd.DataFrame(store_data)
        dropdown_list = ['unidade']
        dropdown_list.extend(df['id_medico'].unique().tolist())
        return dropdown_list

@callback(
    Output('sunburstindicadores', 'figure'),
    Input('dropdown_options', 'value'),
    Input('store_data', 'data'),

)

def sunburst_update(dropdown_options, store_data):

    if store_data is not []:
        df = pd.DataFrame(store_data)
        print(df.columns)


    fig_sunburstindicadores = go.Figure()
    fig_sunburstindicadores.add_trace(go.Sunburst(
        ids=df_sunburst.id,
        labels=df_sunburst.label,
        parents=df_sunburst.parent,
        values=df_sunburst.value,
        branchvalues="total",
        domain=dict(column=1),
        insidetextorientation='radial',
    ))
    fig_sunburstindicadores.update_layout(
        margin=dict(t=0, l=0, r=0, b=0),
        width=800,
        height=800,
    )

    return fig_sunburstindicadores



