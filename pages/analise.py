import dash
from dash import html, dcc, callback, Input, Output, State
from dash.dependencies import Input, Output, State
import base64
import io
import pandas as pd

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
            multiple=False,
        ),
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

@callback(
    Output('store_data', 'data'),
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(list_of_contents, list_of_names):
    if list_of_contents is not None:
        data = []
        for content, name in zip(list_of_contents, list_of_names):
            content_type, content_string = content.split(',')
            decoded = base64.b64decode(content_string)
            try:
                if 'csv' in name:
                    # Assume that the user uploaded a CSV file
                    df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
                elif 'xls' in name:
                    # Assume that the user uploaded an excel file
                    df = pd.read_excel(io.BytesIO(decoded))
                data.append(df.to_dict('records'))
            except Exception as e:
                print(e)
        return data
    return []