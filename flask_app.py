import dash
from dash import Dash, dcc, html, Input, Output, State
import pandas as pd
import dash_bootstrap_components as dbc
import plotly.express as px
#import dash_core_components as dcc
#import dash_html_components as html

# for deployment, pass app.server (which is the actual flask app) to WSGI etc

path = ''
df_indicador = pd.DataFrame(data=pd.read_csv(path + 'indicadores_maio_2022.csv'))

app = dash.Dash(__name__, use_pages=True)

navbar_pages = dbc.Row([
                    dbc.Col([
                        dbc.Nav([
                            dbc.NavItem(dbc.NavLink(page['name'], href=page['path']))
                            for page in dash.page_registry.values()
                        ], navbar=True,)
                    ]),
                ])

navbar = dbc.Navbar([
    dbc.Container([
        html.A(

            dbc.Row([
                    dbc.Col(html.Img(src=app.get_asset_url('LOGO.png'), height="30px")),
                    dbc.Col(dbc.NavbarBrand("BI-MGF", className="ms-2")),
                ], align="center", className="g-0"),
            href="/",
            style={"textDecoration": "none"},
        ),
        dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
        dbc.Collapse(
            navbar_pages,
            id="navbar-collapse",
            is_open=False,
            navbar=True,
        ),
    ]),
], color="dark", dark=True)

app.layout = html.Div([
    navbar,
    dash.page_container,
])
@app.callback(
    Output("navbar-collapse", "is_open"),
    Output("navbar-sunburst_indicadores", "figure"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
)

def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

if __name__ == "__main__":
    app.run(debug=True)