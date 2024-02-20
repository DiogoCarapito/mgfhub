import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# from plotly import data

from utils.etl_relatorios import etiqueta_ano


def check_date(df):
    return df["Mês Ind"].mode()[0]


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


def horizontal_bar_chart(df1, ano1):
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


def dumbbell_plot(dict_dfs, ano):
    # exclude_score_2 = st.radio("Excluir Score = 2", ["Sim", "Não"], index=1)

    dict_figs = {}

    dfs = []
    for nome, each in dict_dfs.items():
        dfs.append(
            {
                "df": each,
                "nome": nome,
                "date": check_date(each),
            }
        )

    # order dfs by date
    dfs = sorted(dfs, key=lambda x: x["date"])

    if len(dict_dfs) == 2:
        # Ensure the dataframes are sorted by 'indicador'
        dfs[0]["df"].sort_values(by="Score", ascending=True, inplace=True)
        dfs[1]["df"].sort_values(by="id", ascending=True, inplace=True)

        # remove the columns that have Dimensão == "IDE"
        dfs[0]["df"] = dfs[0]["df"].loc[dfs[0]["df"]["Dimensão"] != "IDE"]
        dfs[1]["df"] = dfs[1]["df"].loc[dfs[1]["df"]["Dimensão"] != "IDE"]

        # remove the columns that have Nome ==_ "IDE"
        dfs[0]["df"] = dfs[0]["df"].loc[dfs[0]["df"]["Nome"] != "IDE"]
        dfs[1]["df"] = dfs[1]["df"].loc[dfs[1]["df"]["Nome"] != "IDE"]

        list_indicadores = dfs[0]["df"]["Nome"].tolist()

        # Iterate over the 'indicador' values in the first dataframe
        for indicador in list_indicadores:
            # Get the 'Score' values for the current 'indicador' in both dataframes
            score1 = dfs[0]["df"][dfs[0]["df"]["Nome"] == indicador]["Score"].values[0]
            score2 = dfs[1]["df"][dfs[1]["df"]["Nome"] == indicador]["Score"].values[0]

            if score1 != score2:
                marker_info = dict(
                    symbol="arrow",
                    color="grey",
                    size=16,
                    angleref="previous",
                    standoff=8,
                )
            else:
                marker_info = None

            # Create a line from score1 to score2
            line = go.Scatter(
                x=[score1, score2],
                y=[indicador, indicador],
                mode="markers+lines",
                showlegend=False,
                marker=marker_info,
                line=dict(
                    color="grey",
                ),
            )
            dict_figs[indicador] = line

    # colors = ["#588EF9", "#BE1CF3"]

    i = 0

    for nome, df in dict_dfs.items():
        int_aceit, int_esper = etiqueta_ano(df, ano)

        df["Etiqueta"] = nome
        # remove the columns that have Nome ==_ "IDE"
        df = df.loc[df["Nome"] != "IDE"]

        df.sort_values(by="Score", ascending=True, inplace=True)

        dict_figs[nome] = go.Scatter(
            x=df.loc[df["Dimensão"] != "IDE", "Score"],
            y=df.loc[df["Dimensão"] != "IDE", "Nome"],
            mode="markers",
            name=nome,
            marker=dict(
                size=12,
                color=df.loc[df["Dimensão"] != "IDE", "Score"],  # Set color to Score
                colorscale=["#FF7E79", "#FFD479", "#56BA39"],
                symbol=i,  # Set symbol to i
            ),
            customdata=df.loc[
                df["Dimensão"] != "IDE", ["Nome", "Resultado", int_aceit, int_esper]
            ].values,
            hovertemplate="<b>%{customdata[0]}</b><br>Resultado: <b>%{customdata[1]}</b><br>Intervalo Aceitável: %{customdata[2]}<br>Intervalo Esperado: %{customdata[3]}<extra></extra>",
        )
        # iterador de cor
        i += 1

    traces = []
    for trace in dict_figs.values():
        traces.append(trace)

    fig = go.Figure(
        data=traces,
    )

    fig.update_layout(
        xaxis=dict(range=[-0.1, 2.1]),  # minimum value for the x axis
        yaxis=dict(autorange="reversed"),  # reverse the order of the y axis
        height=1200,
        # showlegend=False,
    )

    st.plotly_chart(fig, use_container_width=True)

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


def tabela(df, ano, nome):
    int_aceit, int_esper = etiqueta_ano(df, ano)

    df = df.loc[df["Dimensão"] != "IDE"]

    df_sdm = pd.read_csv(
        "./data/indicadores_sdm_complete.csv", usecols=["id", "link_sdm"]
    )

    df = df.merge(
        df_sdm,
        on="id",
        how="left",
    )

    # make id index
    df.set_index("id", inplace=True)

    # remove row without id
    df = df[df.index.notnull()]

    st.subheader(nome)
    # st.write(df)
    st.dataframe(
        df,
        column_config={
            "link_sdm": st.column_config.LinkColumn(
                label="Link",
                display_text="SDM",
            )
        },
        column_order=[
            "Nome",
            "link_sdm",
            "Dimensão",
            int_aceit,
            int_esper,
            "Resultado",
            "Score",
        ],
        hide_index=False,
    )
    return None
