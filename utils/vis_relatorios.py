import streamlit as st
import plotly.express as px

from utils.etl_relatorios import etiqueta_ano


def sunburst_bicsp(df, ano, size=800):
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
        hovertemplate="""<b>%{customdata[0]}</b><br>Peso: %{value}%<br>Score: <b>%{color:.2f}</b><br>Resultado: <b>%{customdata[1]:.1f}</b><br>Intervalo Esperado: %{customdata[2]}<br>Intervalo Esperado: %{customdata[3]}<extra></extra>""",
        hoverlabel=dict(font=dict(size=14)),
        # hovertext on the lable og the bar
        texttemplate="%{x:.2f}",
        textposition="outside",
        insidetextanchor="start",
    )

    fig.update_layout(
        showlegend=False,
        height=800,
    )

    st.plotly_chart(fig, use_container_width=True)


def horizontal_bar_chart_2(df):
    st.bar_chart(
        df,
        x="Score",
        y="Nome",
        use_container_width=True,
    )
