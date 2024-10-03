import streamlit as st
from utils.etl_relatorios import (
    # etl_bicsp,
    # etl_mimuf,
    # extracao_areas_clinicas,
    # merge_portaria_bicsp,
    process_indicador,
    process_filter_temporal,
)
from utils.vis_relatorios import (
    # sunburst_bicsp,
    # dumbbell_plot,
    # tabela,
    ide_bar,
    horizontal_bar,
    # sunburst_mimuf,
    line_chart,
)


# @st.cache_data
def tab_visao_indicador(df_mimuf):
    (
        col_indicador,
        col_visualizacao,
    ) = st.columns([5, 2])

    with col_indicador:
        list_dfs = list(df_mimuf.keys())
        lista_indicadores = df_mimuf[list_dfs[0]]["df"]["Nome"].unique()
        filtro_indicador = st.selectbox(
            "Indicador",
            (lista_indicadores[1:]),
        )
    with col_visualizacao:
        # radio escolha visualização
        st.session_state["opcao_visualizacao_tab_indicador"] = st.radio(
            "Visualização",
            ["Equipa", "Evolução temporal"],
            horizontal=True,
            key="opcao_visualizacao_indicador",
        )

    if st.session_state["opcao_visualizacao_tab_indicador"] == "Equipa":
        # col_filtro_equipa_1, col_filtro_equipa_2, col_visualizacao = st.columns(
        #     [2, 4, 2]
        # )
        col_filtro_equipa_1, col_visualizacao = st.columns([1, 1])

        with col_filtro_equipa_1:
            dataframe_selected = st.selectbox(
                "Escolha o mês de analise",
                df_mimuf,
            )

        # with col_filtro_equipa_2:
        #     lista_indicadores = df_mimuf[dataframe_selected]["df"]["Nome"].unique()
        #     filtro_indicador = st.selectbox(
        #         "Indicador",
        #         (lista_indicadores[1:]),
        #     )

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
                .sort_values(
                    by=st.session_state["opcao_visualizacao_2"], ascending=False
                )
            )

            st.dataframe(
                df_num_den_med,
                hide_index=True,
            )

    elif st.session_state["opcao_visualizacao_tab_indicador"] == "Evolução temporal":
        data_evolucao_temporal = process_filter_temporal(df_mimuf, filtro_indicador)

        filtro_indicador_id = filtro_indicador.split(" ")[0]
        link = f"https://sdm.min-saude.pt/BI.aspx?id={filtro_indicador_id}"
        text = f"link SDM indicador {filtro_indicador_id}"

        st.markdown(f"[{text}]({link})")

        filtro_visualização = st.radio(
            "Visulaização",
            ["Unidade", "Por profissional"],
            index=0,
            horizontal=True,
            label_visibility="collapsed",
        )
        line_chart(data_evolucao_temporal, filtro_visualização)
