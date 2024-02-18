import pandas as pd
import plotly.express as px
import streamlit as st


def confirmar_ano(df, ano):
    # cria a
    int_aceit = f"Intervalo Aceitável {ano}"
    int_esper = f"Intervalo Esperado {ano}"

    # caso não haja intervalos para o ano dos dados, por definição usa os intervalos de 2023
    if int_aceit not in df.columns or int_esper not in df.columns:
        int_aceit = "Intervalo Aceitável 2023"
        int_esper = "Intervalo Esperado 2023"

    return int_aceit, int_esper


def merge_portaria_bicsp(df_bicsp, ano):
    df_portaria = pd.read_csv("./data/sunburst_portaria_411a_2023.csv")

    # df_portaria.loc[df_portaria["Nome"]=="IDE", "Ponderação"] = 100

    df = df_portaria.merge(
        df_bicsp[["id", "Resultado", "Score"]],
        on="id",
        how="left",
    )

    # list of dimensions and drop empty obnes
    list_dimensoes = [x for x in df["Dimensão"].unique().tolist() if pd.notna(x)]

    # df.loc[~df["Dimensão"].isin(list_dimensoes), :] = df.loc[~df["Dimensão"].isin(list_dimensoes), :].fillna(0)

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
    int_aceit, int_esper = confirmar_ano(df, ano)
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

    df.loc[df["Nome"] != "IDE"] = df.loc[df["Nome"] != "IDE"].fillna(0)

    st.write(
        df[["id", "Nome", "Dimensão", "Ponderação", "Resultado", "Score", "contributo"]]
    )

    return df


def sunburst_bicsp(df_bicsp, ano):
    if df_bicsp is None:
        st.warning("Ficheiro BI-CSP não carregado")
    else:
        # merge do dataframe da portaria com o dataframe vindo do BI-CSP pelo utilizador
        df = merge_portaria_bicsp(df_bicsp, ano)

        int_aceit, int_esper = confirmar_ano(df, ano)

        # sunburst
        fig = px.sunburst(
            df,
            names="Nome",
            parents="Dimensão",
            values="Ponderação",
            branchvalues="total",
            custom_data=["Resultado", int_aceit, int_esper],
            color="Score",
            color_continuous_scale=["#FF7E79", "#FFD479", "#56BA39"],
        )
        fig.update_traces(
            hovertemplate="""<b>%{label}</b><br>Peso: %{value}%<br>Score: <b>%{color:.2f}</b><br>Resultado: <b>%{customdata[0]:.1f}</b><br>Intervalo Esperado: %{customdata[1]}<br>Intervalo Esperado: %{customdata[2]}<extra></extra>""",
            hoverlabel=dict(font=dict(size=18)),
            textinfo="label+percent entry",
            insidetextfont=dict(size=30),
            insidetextorientation="radial",
        )

        fig.update_layout(
            width=800,
            height=800,
            showlegend=False,
        )

        return fig
