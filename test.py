import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd

df = pd.read_excel('data.xlsx', header=2)

app = dash.Dash(__name__)

app.layout = html.Div([
    dbc.Container([
        dcc.Graph(id='sunburst_indicadores', figure=px.sunburst(
            df,
            path=['Hierarquia Contratual - Sub-Área', 'Hierarquia Contratual - Dimensão','Designação Indicador (+ID)'],
            values='Score'
        ))
    ])
])

if __name__ == "__main__":
    app.run(debug=True)