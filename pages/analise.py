import dash
from dash import html, dcc

dash.register_page(
    __name__,
    path="/analise",
    title="analise",
    name="analise",
    order=4,
)

upload = html.Div(
    [
        dcc.Upload(
            id="upload-data",
            children=html.Div(["Drag and Drop or ", html.A("Select Files")]),
            style={
                "width": "100%",
                "height": "60px",
                "lineHeight": "60px",
                "borderWidth": "1px",
                "borderStyle": "dashed",
                "borderRadius": "5px",
                "textAlign": "center",
                "margin": "10px",
            },
            # Allow multiple files to be uploaded
            multiple=True,
        ),
        html.Div(id="output-data-upload"),
    ]
)


container = html.Div(
    [
        html.H3("analise"),
        upload,
    ]
)


def layout():
    return html.Div(
        [
            container,
            html.Br(),
        ]
    )
