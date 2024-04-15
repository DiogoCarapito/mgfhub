import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from utils.etl_relatorios import etiqueta_ano


@st.cache_data()
def check_date(df):
    # check the date of the data
    return df["Mês Ind"].mode()[0]


@st.cache_data()
def remove_dimensao(df):
    # remove rows that have "Dimensão" == "IDE" and "Nome" == "IDE"
    return df.loc[(df["Dimensão"] != "IDE") & (df["Nome"] != "IDE")]


@st.cache_data()
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
        # color_continuous_scale=["#FF7E79", "#FFD479", "#56BA39"], #3 color gradient
        color_continuous_scale=[
            "#FF7E79",
            "#F0A774",
            "#FFD479",
            "#E5CB72",
            "#56BA39",
        ],  # 5 color gradient
    )
    fig.update_traces(
        hovertemplate="""<b>%{customdata[0]}</b><br>Peso: %{value}%<br>Score: <b>%{color:.2f}</b><br>Resultado: <b>%{customdata[1]:.1f}</b><br>Intervalo Aceitável: %{customdata[2]}<br>Intervalo Esperado: %{customdata[3]}<extra></extra>""",
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


# @st.cache_data()
def sunburst_mimuf(df, ano, mes, unidade, size=800):
    ano = 2024
    # get column names for the intervalos aceitáveis e esperados for the selected year
    int_aceit, int_esper = etiqueta_ano(df, ano)
    df = df[df["Score"] != "Error"]

    df_portatia = pd.read_csv("data/sunburst_portaria_411a_2023.csv")

    df = df_portatia.merge(
        df[["id", "Valor", "Score", "Denominador", "Numerador"]],
        on="id",
        how="left",
    )

    # list of dimensions and drop empty obnes
    list_dimensoes = [x for x in df["Dimensão"].unique().tolist() if pd.notna(x)]

    # remove IDE
    list_dimensoes = list_dimensoes[1:]

    # calculate the score for each dimension based on the average wheighed score
    df["contributo"] = df["Ponderação"] * df["Score"] / 2

    for dim in list_dimensoes:
        df.loc[df["Nome"] == dim, "Resultado"] = df[df["Dimensão"] == dim][
            "contributo"
        ].sum()

    df.loc[df["Dimensão"] == "IDE", "Score"] = (
        2
        * df.loc[df["Dimensão"] == "IDE", "Resultado"]
        / df.loc[df["Dimensão"] == "IDE", "Ponderação"]
    )

    # apagar intervalos que não fazem sentido
    int_aceit, int_esper = etiqueta_ano(df, ano)
    df.loc[df["Dimensão"] == "IDE", int_aceit] = "N/A"
    df.loc[df["Dimensão"] == "IDE", int_esper] = "N/A"
    df.loc[df["Nome"] == "IDE", int_aceit] = "N/A"
    df.loc[df["Nome"] == "IDE", int_esper] = "N/A"

    # IDE
    df.loc[df["Nome"] == "IDE", "Resultado"] = df.loc[
        df["Dimensão"] == "IDE", "Resultado"
    ].sum()
    df.loc[df["Nome"] == "IDE", "Score"] = (
        2
        * df.loc[df["Nome"] == "IDE", "Resultado"]
        / df.loc[df["Nome"] == "IDE", "Ponderação"]
    )

    # df.loc[df["Nome"] != "IDE"] = df.loc[df["Nome"] != "IDE"].fillna(0)

    # make score a float
    df["Score"] = df["Score"].astype(float)

    # Add a row with Score 0
    df = df.append(
        {
            "Lable": "",
            "Dimensão": "",
            "Ponderação": 0,
            "Nome": "",
            "Valor": "",
            int_aceit: "",
            int_esper: "",
            "Score": 0,
        },
        ignore_index=True,
    )

    # Add a row with Score 2
    df = df.append(
        {
            "Lable": "",
            "Dimensão": "",
            "Ponderação": 0,
            "Nome": "",
            "Valor": "",
            int_aceit: "",
            int_esper: "",
            "Score": 2,
        },
        ignore_index=True,
    )

    # sunburst
    fig = px.sunburst(
        df,
        names="Lable",
        parents="Dimensão",
        values="Ponderação",
        branchvalues="total",
        custom_data=["Nome", "Valor", int_aceit, int_esper],
        color="Score",
        # color_continuous_scale=["#FF7E79", "#FFD479", "#56BA39"],
        color_continuous_scale=[
            "#FF7E79",
            "#F0A774",
            "#FFD479",
            "#E5CB72",
            "#56BA39",
        ],  # 5 color gradient
        range_color=[0, 2],
    )
    fig.update_traces(
        hovertemplate="""<b>%{customdata[0]}</b><br>Peso: %{value}%<br>Score: <b>%{color:.2f}</b><br>Resultado: <b>%{customdata[1]:.2f}</b><br>Intervalo Aceitável: %{customdata[2]}<br>Intervalo Esperado: %{customdata[3]}<extra></extra>""",
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


@st.cache_data()
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
        # color_continuous_scale=["#FF7E79", "#FFD479", "#56BA39"],
        color_continuous_scale=[
            "#FF7E79",
            "#F0A774",
            "#FFD479",
            "#E5CB72",
            "#56BA39",
        ],  # 5 color gradient
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


@st.cache_data()
def dumbbell_plot(dict_dfs, ano):
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

            if abs(score1 - score2) < 0.06:
                marker_info = None
                linecolor = "grey"

            elif score1 > score2:
                marker_info = dict(
                    symbol="arrow",
                    # color="#FF7E79",
                    color="grey",
                    size=18,
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
                    size=18,
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

        # drop rows if "Score" is  None
        each["df"] = each["df"].dropna(subset=["Score"])

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
                # size=16,
                size=10 * np.sqrt(each["df"]["Ponderação"]),
                color=each["df"]["Score"],  # Set color to Score
                # colorscale=["#FF7E79", "#FFD479", "#56BA39"],
                colorscale=[
                    "#FF7E79",
                    "#F0A774",
                    "#FFD479",
                    "#E5CB72",
                    "#56BA39",
                ],  # 5 color gradient
                symbol=i + 0,  # Set symbol to i
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


@st.cache_data()
def tabela(df, ano, nome):
    ano = 2024
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

    # remove rows where Score is None
    df = df.dropna(subset=["Score"])

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
            "Ponderação",
            int_aceit,
            int_esper,
            "Resultado",
            "Score",
        ],
        hide_index=False,
    )
    return None


@st.cache_data()
def horizontal_bar(df, ano, ordenar_por):
    ano = 2024

    df.dropna(subset=["id"], inplace=True)

    df.sort_values(by=ordenar_por, ascending=True, inplace=True)

    freq = df["Valor"].round(1)

    med = df["Médico Familia"]

    nome = df["Nome"].unique()[0]

    min_aceitavel = df[f"Mínimo Aceitável {ano}"].unique()[0]
    min_esperado = df[f"Mínimo Esperado {ano}"].unique()[0]
    max_aceitavel = df[f"Máximo Aceitável {ano}"].unique()[0]
    max_esperado = df[f"Máximo Esperado {ano}"].unique()[0]
    minimo = 0

    maximo_medico = df.groupby("Médico Familia")["Valor"].max().max()

    # se é o indicador 314, defenir o máximo com 100
    # porque o 314 é um indicador que e está mal desenhado! or 354

    if df["id"].unique()[0] == 314 or df["id"].unique()[0] == 354:
        maximo = 100
    elif df["id"].unique()[0] == 404:
        if maximo_medico > 100:
            maximo, max_esperado, max_aceitavel = (
                maximo_medico,
                maximo_medico,
                maximo_medico,
            )
        else:
            maximo, max_esperado, max_aceitavel = 100, 100, 100
    else:
        maximo = max([min_aceitavel, min_esperado, max_esperado, max_aceitavel])

    # Define the colors
    colors = ["red", "yellow", "green", "yellow", "red"]

    # Define the ranges of the colors
    ranges = [
        (minimo, min_aceitavel),
        (min_aceitavel, min_esperado),
        (min_esperado, max_esperado),
        (max_esperado, max_aceitavel),
        (max_aceitavel, maximo),
    ]

    fig, ax = plt.subplots(figsize=(8, 6))

    # Add the background areas
    for color, (start, end) in zip(colors, ranges):
        ax.axvspan(start, end, facecolor=color, alpha=0.3)

    bar = ax.barh(med, freq, color=(30 / 255, 75 / 255, 124 / 255, 1))

    # Set plot title and labels
    ax.set_title(f"{nome} por MF")
    ax.set_xlabel("Cumprimento")
    ax.set_ylabel("Médico Familia")

    ax.set_xlim(minimo, maximo)

    ax.set_xticks(
        [minimo, min_aceitavel, min_esperado, max_esperado, max_aceitavel, maximo]
    )

    for rect in bar:
        width = rect.get_width()
        ax.text(
            width,
            rect.get_y() + rect.get_height() / 2,
            f"{width}%",
            ha="left",
            va="center",
        )

    st.pyplot(fig)


@st.cache_data()
def stakced_barchart(df):
    med = df["Médico Familia"]
    # denominador = df["Denominador"]
    numerador = df["Numerador"].astype(int)

    df["falta"] = df["Denominador"].astype(int) - df["Numerador"].astype(int)
    falta = df["falta"].astype(int)

    fig, ax = plt.subplots(figsize=(8, 6))

    ax.barh(med, numerador, color="green")
    ax.barh(med, falta, left=falta, color="red")

    ax.set_xlabel("Denominador")
    ax.set_ylabel("Médico Familia")
    ax.set_title("Denominador and Numerador by Médico Familia")

    st.pyplot(fig)
