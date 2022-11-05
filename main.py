import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, State, html

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SIMPLEX])

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
                dbc.Col(html.Img(src=app.get_asset_url('LOGO_2.png'), height='30px')),
                dbc.Col(dbc.NavbarBrand('bi-indicadores', className='ms-2')),
                ], align='center', className='g-0'),
            href='/',
            style={'textDecoration': 'none'},
        ),
        dbc.NavbarToggler(id='navbar-toggler', n_clicks=0),
        dbc.Collapse(
            navbar_pages,
            id='navbar-collapse',
            is_open=False,
            navbar=True,
        ),
    ], fluid=True,),
],
    color='light',
    dark=False,
    fixed='top',
)

app.layout = html.Div([
    navbar,
    html.Br(),
    html.Br(),
    html.Br(),
    html.Br(),
    dash.page_container,
])


@app.callback(
    Output('navbar-collapse', 'is_open'),
    Input('navbar-toggler', 'n_clicks'),
    State('navbar-collapse', 'is_open')
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


if __name__ == '__main__':
    app.run(debug=True)
