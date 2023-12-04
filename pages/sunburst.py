import dash
from dash import html, dcc

# callback, Output, Input
import dash_bootstrap_components as dbc
import pandas as pd

import plotly.graph_objects as go
import plotly.io as pio


pio.templates.default = "seaborn"
# seaborn
# presentation

dash.register_page(
    __name__,
    path="/sunburst",
    title="sunburst",
    name="sunburst",
    order=3,
)

df_sunburst = pd.read_csv("scripts/sunburst_data_contrat.csv")

# lines where operacionalizar is false
# df_sunburst = df_sunburst[df_sunburst["operacionalizar"] == True]

# create figure
fig_sunburst_indicadores = go.Figure()

fig_sunburst_indicadores.add_trace(
    go.Sunburst(
        ids=df_sunburst["name"],
        labels=df_sunburst["label"],
        parents=df_sunburst["parent"],
        values=df_sunburst["value"],
        # values=df_sunburst["valor_operacionalizado"],
        branchvalues="total",
        domain=dict(column=1),
        insidetextorientation="radial",
        hovertemplate="<b>%{label} </b> <br> peso: %{value:.2f}%",
    )
)

fig_sunburst_indicadores.update_layout(
    margin=dict(t=0, l=0, r=0, b=0),
    width=800,
    height=800,
)


header = html.Div(
    (
        dbc.Row(
            [
                html.H3("sunburst"),
            ]
        ),
    )
)

graphs = html.Div(
    [
        dbc.Row(
            [
                dbc.Col([], width=1),
                dbc.Col([dcc.Graph(figure=fig_sunburst_indicadores)], width=10),
                dbc.Col([], width=1),
            ]
        ),
    ]
)
container = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(
                    [
                        header,
                        graphs,
                        html.Br(),
                    ]
                )
            ]
        )
    ],
    fluid=True,
)


def layout():
    return html.Div(
        [
            container,
            html.Br(),
        ]
    )
