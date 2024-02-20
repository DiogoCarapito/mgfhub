import streamlit as st
import plotly.express as px

# import plotly.graph_objects as go
# from plotly import data

from utils.etl_relatorios import etiqueta_ano


def sunburst_bicsp(df, ano, mes, unidade, size=800):
    # get column names for the intervalos aceitáveis e esperados for the selected year
    int_aceit, int_esper = etiqueta_ano(df, ano)

    # sunburst
    fig = px.sunburst(
        df,
        names="Lable",
        parents="Dimensão",
        values="Ponderação",
        branchvalues="total",
        custom_data=["Nome", "Resultado", int_aceit, int_esper],
        color="Score",
        color_continuous_scale=["#FF7E79", "#FFD479", "#56BA39"],
    )
    fig.update_traces(
        hovertemplate="""<b>%{customdata[0]}</b><br>Peso: %{value}%<br>Score: <b>%{color:.2f}</b><br>Resultado: <b>%{customdata[1]:.1f}</b><br>Intervalo Esperado: %{customdata[2]}<br>Intervalo Esperado: %{customdata[3]}<extra></extra>""",
        hoverlabel=dict(font=dict(size=18)),
        textinfo="label",
        insidetextfont=dict(size=24),
        insidetextorientation="radial",
    )

    fig.update_layout(
        title=f"{unidade} {mes}/{ano}",
        title_font=dict(size=24),
        width=size,
        height=size,
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True)


def horizontal_bar_chart(
    df1,
    ano1,
):
    # get column names for the intervalos aceitáveis e esperados for the selected year
    int_aceit, int_esper = etiqueta_ano(df1, ano1)

    df1["Lable"] = df1["Lable"].astype(str)

    df1.sort_values(by="Score", ascending=False, inplace=True)

    fig = px.bar(
        df1.loc[df1["Dimensão"] != "IDE"],
        x="Score",
        y="Nome",
        orientation="h",
        color="Score",
        color_continuous_scale=["#FF7E79", "#FFD479", "#56BA39"],
        custom_data=["Nome", "Resultado", int_aceit, int_esper],
        # miminum valiu for the x axis
        range_x=[0, 2.3],
    )

    fig.update_traces(
        hovertemplate="""<b>%{customdata[0]}</b><br>Peso: %{value}%<br>Score: <b>%{color:.3f}</b><br>Resultado: <b>%{customdata[1]:.1f}</b><br>Intervalo Esperado: %{customdata[2]}<br>Intervalo Esperado: %{customdata[3]}<extra></extra>""",
        hoverlabel=dict(font=dict(size=14)),
        # hovertext on the lable og the bar
        texttemplate="%{x:.2f}",
        textposition="outside",
        insidetextanchor="start",
    )

    fig.update_layout(
        title="unidade",
        showlegend=False,
        height=800,
    )

    st.plotly_chart(fig, use_container_width=True)


def dumbbell_plot():
    # df = data.gapminder()
    # df = df.loc[(df.continent == "Europe") & (df.year.isin([1952, 2002]))]

    # countries = (
    #     df.loc[(df.continent == "Europe") & (df.year.isin([2002]))]
    #     .sort_values(by=["lifeExp"], ascending=True)["country"]
    #     .unique()
    # )

    # data = {
    #     "line_x": [],
    #     "line_y": [],
    #     "1952": [],
    #     "2002": [],
    #     "colors": [],
    #     "years": [],
    #     "countries": [],
    # }

    # for country in countries:
    #     data["1952"].extend(
    #         [df.loc[(df.year == 1952) & (df.country == country)]["lifeExp"].values[0]]
    #     )
    #     data["2002"].extend(
    #         [df.loc[(df.year == 2002) & (df.country == country)]["lifeExp"].values[0]]
    #     )
    #     data["line_x"].extend(
    #         [
    #             df.loc[(df.year == 1952) & (df.country == country)]["lifeExp"].values[
    #                 0
    #             ],
    #             df.loc[(df.year == 2002) & (df.country == country)]["lifeExp"].values[
    #                 0
    #             ],
    #             None,
    #         ]
    #     )
    #     data["line_y"].extend([country, country, None]),

    # fig = go.Figure(
    #     data=[
    #         go.Scatter(
    #             x=data["line_x"],
    #             y=data["line_y"],
    #             mode="markers+lines",
    #             showlegend=False,
    #             marker=dict(
    #                 symbol="arrow",
    #                 color="black",
    #                 size=16,
    #                 angleref="previous",
    #                 standoff=8,
    #             ),
    #         ),
    #         go.Scatter(
    #             x=data["1952"],
    #             y=countries,
    #             name="1952",
    #             mode="markers",
    #             marker=dict(
    #                 color="silver",
    #                 size=16,
    #             ),
    #         ),
    #         go.Scatter(
    #             x=data["2002"],
    #             y=countries,
    #             name="2002",
    #             mode="markers",
    #             marker=dict(
    #                 color="lightskyblue",
    #                 size=16,
    #             ),
    #         ),
    #     ]
    # )

    # fig.update_layout(
    #     title="Life Expectancy in Europe: 1952 and 2002",
    #     height=1000,
    #     legend_itemclick=False,
    # )

    # fig.show()
    return None
