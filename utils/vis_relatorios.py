import pandas as pd
import plotly.express as px


def sunburst_bicsp(df_bicsp):
    if df_bicsp is None:
        # load the pre-processed data
        df_portaria = pd.read_csv("./data/sunburst_portaria_411a_2023.csv")

        # sunburst
        fig = px.sunburst(
            df_portaria,
            names="Nome",
            parents="Dimensão",
            values="Ponderação",
            branchvalues="total",
            custom_data="id",
            # color="Ponderação",
            # color_continuous_scale="RdBu",
        )
        fig.update_traces(
            hovertemplate="<br><b>%{label}</b><br>Ponderação: %{value}<extra></extra>",
            # hoverinfo="label+percent entry",
            textinfo="label+percent entry",
            insidetextorientation="radial",
        )

        fig.update_layout(
            # autosize=True,
            width=600,
            height=600,
        )
        return fig
