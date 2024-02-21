import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# from plotly import data

from utils.etl_relatorios import etiqueta_ano


def check_date(df):
    # check the date of the data
    return df["Mês Ind"].mode()[0]


def remove_dimensao(df):
    # remove rows that have "Dimensão" == "IDE" and "Nome" == "IDE"
    return df.loc[(df["Dimensão"] != "IDE") & (df["Nome"] != "IDE")]


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
    col_filter_dumbbell_1, col_filter_dumbbell_2 = st.columns([1, 1])
    with col_filter_dumbbell_1:
        slider_peso = st.slider(
            "Filtrar por Peso",
            min_value=0.0,
            max_value=10.0,
            value=[0.0, 10.0],
            step=0.1,
            # help="Escolha o peso que pretende para a métrica",
        )
    with col_filter_dumbbell_2:
        st.empty()
        # exclude_score_2 = st.radio("Excluir Score = 2", ["Sim", "Não"], horizontal=True, index=1, disabled=True)

    dict_figs = {}

    dfs = []
    for nome, each in dict_dfs.items():
        dfs.append(
            {
                "df": remove_dimensao(each),
                "nome": nome,
                "date": check_date(each),
            }
        )

    # order dfs by date
    dfs = sorted(dfs, key=lambda x: x["date"])

    # filter by peso
    for each in dfs:
        each["df"] = each["df"].loc[
            (each["df"]["Ponderação"] >= slider_peso[0])
            & (each["df"]["Ponderação"] <= slider_peso[1])
        ]

    if len(dict_dfs) == 2:
        # Ensure the dataframes are sorted by 'indicador'
        dfs[0]["df"].sort_values(by="Score", ascending=True, inplace=True)
        dfs[1]["df"].sort_values(by="Score", ascending=True, inplace=True)

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

            if abs(score1 - score2) < 0.1:
                marker_info = None
                linecolor = None

            elif score1 > score2:
                marker_info = dict(
                    symbol="arrow",
                    # color="#FF7E79",
                    color="grey",
                    size=20,
                    angleref="previous",
                    standoff=8,
                )
                # linecolor = "#FF7E79"
                linecolor = "grey"
            else:
                marker_info = dict(
                    symbol="arrow",
                    # color="#56BA39",
                    color="grey",
                    size=20,
                    angleref="previous",
                    standoff=8,
                )
                # linecolor = "#56BA39"
                linecolor = "grey"

            # Create a line from score1 to score2
            line = go.Scatter(
                x=[score1, score2],
                y=[indicador, indicador],
                mode="markers+lines",
                showlegend=False,
                marker=marker_info,
                line=dict(
                    color=linecolor,
                ),
                hoverinfo="none",  # disable hover
            )
            dict_figs[indicador] = line

    # colors = ["#588EF9", "#BE1CF3"]

    i = 0

    for each in dfs:
        int_aceit, int_esper = etiqueta_ano(each["df"], ano)

        each["df"]["Etiqueta"] = each["nome"]
        # remove the columns that have Nome ==_ "IDE"
        each["df"] = each["df"].loc[each["df"]["Nome"] != "IDE"]
        each["df"] = each["df"].loc[each["df"]["Dimensão"] != "IDE"]

        each["df"].sort_values(by="Score", ascending=True, inplace=True)

        dict_figs[each["nome"]] = go.Scatter(
            x=each["df"]["Score"],
            y=each["df"]["Nome"],
            mode="markers",
            name=each["nome"],
            marker=dict(
                size=16,
                color=each["df"]["Score"],  # Set color to Score
                colorscale=["#FF7E79", "#FFD479", "#56BA39"],
                symbol=i + 1,  # Set symbol to i
            ),
            customdata=each["df"][
                ["Nome", "Resultado", int_aceit, int_esper, "Score", "Ponderação"]
            ].values,
            hovertemplate="<b>%{customdata[0]}</b><br>Peso: %{customdata[5]}%<br>Score: <b>%{customdata[4]:.3f}</b><br>Resultado: <b>%{customdata[1]:.1f}</b><br>Intervalo Aceitável: %{customdata[2]}<br>Intervalo Esperado: %{customdata[3]}<extra></extra>",
            hoverlabel=dict(font=dict(size=18)),
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
        xaxis=dict(
            range=[-0.1, 2.1],  # minimum and maximum values for the x axis
            tickvals=[
                0,
                0.5,
                1,
                1.5,
                2,
            ],  # specify the values at which ticks should appear
            ticklen=10,  # length of the ticks
            showgrid=True,  # show grid lines
            gridcolor="#D3D3D3",  # set grid color to light grey
            gridwidth=1,  # set grid line width
            tickfont=dict(size=20),  # increase the size of the x axis labels
            side="bottom",  # position the x axis labels at the top
        ),
        yaxis=dict(
            autorange="reversed",  # reverse the order of the y axis
            tickfont=dict(size=18),  # increase the size of the y axis labels
        ),
        height=each["df"].shape[0] * 25 + 300,
        # showlegend=False,
        legend=dict(
            orientation="h",  # horizontal orientation
            yanchor="bottom",  # anchor the y position to the bottom
            y=1.02,  # position the y just above the top of the graph
            xanchor="right",  # anchor the x position to the right
            x=1,  # position the x at the far right of the graph
            font=dict(size=14),  # increase the size of the legend labels
        ),
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
