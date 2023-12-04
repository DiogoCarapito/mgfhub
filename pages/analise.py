import dash
from dash import html

dash.register_page(
    __name__,
    path="/analise",
    title="analise",
    name="analise",
    order=4,
)

container = html.Div(
    html.H1("analise"),
)


def layout():
    return html.Div(
        [
            container,
            html.Br(),
        ]
    )
