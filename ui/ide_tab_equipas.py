import streamlit as st
from utils.etl_relatorios import (
    # etl_bicsp,
    # etl_mimuf,
    # extracao_areas_clinicas,
    # merge_portaria_bicsp,
    process_indicador,
)
from utils.vis_relatorios import (
    # sunburst_bicsp,
    # dumbbell_plot,
    # tabela,
    ide_bar,
    horizontal_bar,
    # sunburst_mimuf,
)


# @st.cache_data
def tab_visao_equipas(df_mimuf):
    col_filtro_equipa_1, col_filtro_equipa_2, col_visualizacao = st.columns([1, 3, 2])

    with col_filtro_equipa_1:
        dataframe_selected = st.selectbox(
            "Escolha o mês de analise",
            df_mimuf,
        )

    with col_filtro_equipa_2:
        lista_indicadores = df_mimuf[dataframe_selected]["df"]["Nome"].unique()
        filtro_indicador = st.selectbox(
            "Indicador",
            (lista_indicadores[1:]),
        )

    with col_visualizacao:
        st.session_state["opcao_visualizacao_2"] = st.radio(
            "Ordenar por:",
            ["Valor", "Numerador", "Denominador"],
            index=1,
            horizontal=True,
        )

    st.divider()

    # processarinfomração por médico para unidade
    valores_indicador = process_indicador(
        df_mimuf[dataframe_selected]["df"].loc[
            df_mimuf[dataframe_selected]["df"]["Nome"] == filtro_indicador
        ]
    )

    # visualização barra horizontal com os valores indicador
    ide_bar_col_1, ide_bar_col_2, ide_bar_col_3 = st.columns([3, 1, 1])

    with ide_bar_col_1:
        ide_bar(valores_indicador)

    with ide_bar_col_2:
        st.metric(
            "Quanto faltam até aceitável",
            valores_indicador["quantos_faltam_aceitavel"],
            help="Quanto falta para atingir o valor aceitável para o indicador (se positivo, já ultrapassou o valor aceitável, corresponde ao número de utentes que o valor do indicador é superior ao valor aceitável)",
        )

    with ide_bar_col_3:
        st.metric(
            "Quanto faltam até esperado",
            valores_indicador["quantos_faltam_esperado"],
            help="Quanto falta para atingir o valor esperado para o indicador (se positivo, já ultrapassou o valor esperado, corresponde ao número de utentes que o valor do indicador é superior ao valor esperado)",
        )

    col_graph_1, col_graph_2 = st.columns([5, 3])

    with col_graph_1:
        horizontal_bar(
            df_mimuf[dataframe_selected]["df"].loc[
                df_mimuf[dataframe_selected]["df"]["Nome"] == filtro_indicador
            ],
            df_mimuf[dataframe_selected]["ano"],
            st.session_state["opcao_visualizacao_2"],
        )

    with col_graph_2:
        # link for sdm by using th id of the indicador selected
        # extract the initial numbers inside this string
        filtro_indicador_id = filtro_indicador.split(" ")[0]
        link = f"https://sdm.min-saude.pt/BI.aspx?id={filtro_indicador_id}"
        text = f"link SDM indicador {filtro_indicador_id}"

        st.markdown(f"[{text}]({link})")

        df_num_den_med = (
            df_mimuf[dataframe_selected]["df"]
            .loc[df_mimuf[dataframe_selected]["df"]["Nome"] == filtro_indicador][
                ["Médico Familia", "Numerador", "Denominador", "Valor"]
            ]
            .sort_values(by=st.session_state["opcao_visualizacao_2"], ascending=False)
        )

        st.dataframe(
            df_num_den_med,
            hide_index=True,
        )

    # st.divider()

    # st.subheader("Cálculo de estimativas")

    # col_metric_1, col_metric_2, col_metric_3, col_metric_4 = st.columns(4)

    # numerador = df_num_den_med["Numerador"].sum().astype(int)
    # denominador = df_num_den_med["Denominador"].sum().astype(int)

    # with col_metric_1:
    #     num = st.number_input("Numerador", value=numerador, key="numerador", step=10)

    # with col_metric_2:
    #     den = st.number_input(
    #         "Denominador", value=denominador, key="denominador", step=10
    #     )

    # with col_metric_3:
    #     # calcular valor
    #     valor = round(num / den * 100, 2)

    #     st.metric("Valor Estimado", valor)

    # with col_metric_4:
    #     st.metric("Valor Actual", round(numerador / denominador * 100, 2))
