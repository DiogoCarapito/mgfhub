import dash_bootstrap_components as dbc
from dash import Dash, page_registry, page_container, Input, Output, State, html, dcc


# Boostrap theme
bs = "https://cdn.jsdelivr.net/npm/bootswatch@5.2.3/dist/simplex/bootstrap.min.css"

# Register pages
app = Dash(
    __name__,
    use_pages=True,
    suppress_callback_exceptions=True,
    external_stylesheets=[bs, dbc.icons.BOOTSTRAP],
)

# App title
app.title = "mgfhub"


# Navbar pages
navbar_pages = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Nav(
                    [
                        dbc.NavItem(dbc.NavLink(page["name"], href=page["path"]))
                        for page in page_registry.values()
                    ]
                    + [
                        dbc.NavItem(
                            dbc.NavLink(
                                html.I(
                                    html.Img(
                                        src=app.get_asset_url(
                                            "Diogo DALL-E circle 256.png"
                                        ),
                                        height="18px",
                                    )
                                ),
                                href="https://diogocarapito.com",
                                external_link=True,
                            )
                        ),
                    ]
                    + [
                        dbc.NavItem(
                            dbc.NavLink(
                                html.I(
                                    # children='source code',
                                    className="bi bi-twitter"
                                ),
                                href="https://twitter.com/DiogoCarapito",
                                external_link=True,
                            )
                        ),
                    ]
                    + [
                        dbc.NavItem(
                            dbc.NavLink(
                                html.I(
                                    # children='source code',
                                    className="bi bi-github"
                                ),
                                href="https://github.com/DiogoCarapito",
                                external_link=True,
                            )
                        ),
                    ]
                    + [
                        dbc.NavItem(
                            dbc.NavLink(
                                html.I(
                                    # children='source code',
                                    className="bi bi-linkedin"
                                ),
                                href="https://www.linkedin.com/in/diogo-carapito-564a51262/",
                                external_link=True,
                            )
                        ),
                    ],
                    navbar=True,
                )
            ]
        ),
    ]
)

# Navbar
navbar = dbc.Navbar(
    [
        dbc.Container(
            [
                html.A(
                    dbc.Row(
                        [
                            dbc.Col(
                                html.Img(
                                    src=app.get_asset_url("logo.png"), height="30px"
                                )
                            ),
                            dbc.Col(dbc.NavbarBrand("mgfhub", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
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
            ],
            fluid=True,
        ),
    ],
    color="light",
    dark=False,
    fixed="top",
)

app.layout = html.Div(
    [
        navbar,
        html.Br(),
        html.Br(),
        html.Br(),
        html.Br(),
        dbc.Container(
            [
                page_container,
            ]
        ),
        dcc.Store(id="store_data", data=[], storage_type="memory"),
    ]
)


## Falta um callback para ler o click num navlink e fechar o navbar-toggle
@app.callback(
    Output("navbar-collapse", "is_open"),
    Input("navbar-toggler", "n_clicks"),
    State("navbar-collapse", "is_open"),
)

# Função para gerir o botão navbar colapse
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


server = app.server

# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
