import streamlit as st
from utils.etl_relatorios import etl_bicsp, etl_mimuf, extracao_areas_clinicas

from utils.etl_relatorios import merge_portaria_bicsp
from utils.vis_relatorios import (
    sunburst_bicsp,
    dumbbell_plot,
    tabela,
    horizontal_bar,
    sunburst_mimuf,
)


# Sidebar with uplods of xlsx files


def ide_sidebar():
    with st.sidebar:
        # upload de xlsx de bicsp
        st.markdown(
            "## Upload do excel do [BI-CSP](https://bicsp.min-saude.pt/pt/contratualizacao/idg/Paginas/default.aspx)"
        )

        # Upload de ficheiro excel do BI-CSP
        uploaded_file_bicsp = st.file_uploader(
            "Upload excel proveniente do BI-CSP",
            type=["xlsx"],
            # help="Ajuda BI-CSP",
            label_visibility="collapsed",
            accept_multiple_files=True,
        )

        st.markdown(
            "[Como extrair o ficheiro excel do BI-CSP?](https://mgfhub.com/FAQs)",
            unsafe_allow_html=True,
        )
        st.markdown(
            '(Já é possível extrair o ficheiro do BI-CSP na nova secção do [IDE](https://bicsp.min-saude.pt/pt/contratualizacao/ide/Paginas/default.aspx), separador "Dimensões e Indicadores IDE")'
        )

        # st.write("")

        # upload de xlsx de mimuf
        st.markdown("## Upload do excel do MIMUF")

        # Upload de ficheiro excel do MIMUF
        uploaded_file_mimuf = st.file_uploader(
            "Upload excel proveniente do MIM@UF",
            type=["xlsx"],
            # help="Ajuda MIMUF",
            label_visibility="collapsed",
            accept_multiple_files=True,
        )

        st.markdown(
            "[Como extrair o ficheiro excel do MIM@UF?](https://mgfhub.com/FAQs)",
            unsafe_allow_html=True,
        )

        st.write("")

        with st.expander("Dicas"):
            st.markdown(
                "**1 -** Podes carregar mais do que um ficheiro do BI-CSP e/ou MIM@UF com periodos diferentes. Permite comparar diferentes periodos e/ou unidades."
            )
            st.markdown(
                "**2 -** Depois de extrarir uma vez os ficheitos do BI-CSP/MIM@UF no mês, podes guardar nas pastas partilhadas da unidade para utlilizar novamente, uma vez que os dados não ficam guardados no servidor do mgfhub."
            )

        post_etl_bicsp = etl_bicsp(uploaded_file_bicsp)

        post_etl_mimuf = etl_mimuf(uploaded_file_mimuf)

    return post_etl_bicsp, post_etl_mimuf


# @st.cache_data
def tab_visao_unidade(df_bicsp):
    opções_visualizacao = (
        [
            "Sunburst",
            "Tabela",
            "Sunburst + Tabela",
            "Dumbbell",
            "Sunburst + Sunburst",
        ]
        if len(df_bicsp) > 1
        else ["Sunburst", "Tabela", "Sunburst + Tabela", "Dumbbell"]
    )
    # Dumbbell chart by default if more than one file uploaded
    index_visualizacao = 3 if len(df_bicsp) > 1 else 0

    # radio escolha visualização
    st.session_state["opcao_visualizacao"] = st.radio(
        "Visualização",
        opções_visualizacao,
        horizontal=True,
        index=index_visualizacao,
        # label_visibility="collapsed",
        key="opcao_visualizacao_1",
    )

    # st.divider()

    # filtros
    col_filter_1, col_filter_2, col_filter_3, col_filter_4 = st.columns([2, 1, 2, 1])

    # escolha do dataframe de analise
    with col_filter_1:
        escolha = st.selectbox("Escolha o dados para análise", df_bicsp)

    if st.session_state["opcao_visualizacao"] is not "Dumbbell":
        # st.divider()
        col_2_filter_1, col_2_filter_2, col_2_filter_3 = st.columns([2, 1, 1])
        # filtro de areas clinicas
        # get the unique values of "Área clínica" from the dataframe
        areas_clinicas = extracao_areas_clinicas(df_bicsp[escolha]["data"])

        with col_2_filter_1:
            # selectbox for the "Área clínica"
            selected_areas = st.multiselect(
                "Área clínica", areas_clinicas, help="Filtrar por área clínica"
            )

        with col_2_filter_2:
            score_range = st.slider(
                "Score", 0.0, 2.0, (0.0, 2.0), 0.1, help="Filtrar por score (0-2)"
            )

        with col_2_filter_3:
            ponderacao_range = st.slider(
                "Peso",
                1.2,
                10.0,
                (1.2, 10.0),
                0.2,
                help="Filtrar por peso do indicador",
            )

        # if selected_areas is not empty, filter the dataframe and update df_bicsp

        for key, value in df_bicsp.items():
            # make Score None if score not in the range
            mask = (value["data"]["Score"] < score_range[0]) | (
                value["data"]["Score"] > score_range[1]
            )
            value["data"].loc[mask, "Score"] = None

            if selected_areas:
                # substitute the value in "Score" to None if the "Área clínica" is not in the selected_areas
                mask = value["data"]["Área clínica"].isin(selected_areas)
                value["data"].loc[~mask, "Score"] = None

            # update df_bicso with the new value
            df_bicsp[key] = value

    # processamento do dataframe
    df_sunburst = merge_portaria_bicsp(
        df_bicsp[escolha]["data"],
        df_bicsp[escolha]["ano"],
    )

    if st.session_state["opcao_visualizacao"] is not "Dumbbell":
        # Change score to None if Ponderação is not in the ponderacao_range and Hierarquia is 'IDE- Desempenho'
        mask = (
            (df_sunburst["Ponderação"] < ponderacao_range[0])
            | (df_sunburst["Ponderação"] > ponderacao_range[1])
        ) & (df_sunburst["Hierarquia Contratual - Área"] == "IDE - Desempenho")
        df_sunburst.loc[mask, "Score"] = None

    # metrica IDE
    with col_filter_2:
        ide = (
            (
                df_sunburst.loc[
                    (df_sunburst["Nome"] == "IDE") & (df_sunburst["Score"].notnull()),
                    "Resultado",
                ]
                .values[0]
                .round(1)
            )
            if df_sunburst.loc[df_sunburst["Nome"] == "IDE", "Score"].notnull().any()
            else None
        )
        # max_ide = df_sunburst.loc[(df_sunburst["Nome"] == "IDE") & (df_sunburst["Score"].notnull()), "Ponderação"].sum().round(1)
        # perda_ide = max_ide - ide

        st.metric("IDE", ide)

    # SUNBURST
    if st.session_state["opcao_visualizacao"] == "Sunburst":
        # if len(df_bicsp) == 1:
        sunburst_bicsp(
            df_sunburst,
            df_bicsp[escolha]["ano"],
            df_bicsp[escolha]["mes"],
            df_bicsp[escolha]["unidade"],
            800,
        )

    # TABELA
    if st.session_state["opcao_visualizacao"] == "Tabela":
        # tabela
        if len(df_bicsp) >= 1:
            # st.write(df_sunburst[["Nome", "Resultado", "Score"]])
            tabela(
                df_sunburst,
                df_bicsp[escolha]["ano"],
                df_bicsp[escolha]["nome"],
            )

    # SUNBURST + TABELA
    if st.session_state["opcao_visualizacao"] == "Sunburst + Tabela":
        col_1, col_2 = st.columns([1, 1])
        with col_1:
            sunburst_bicsp(
                df_sunburst,
                df_bicsp[escolha]["ano"],
                df_bicsp[escolha]["mes"],
                df_bicsp[escolha]["unidade"],
                500,
            )
        with col_2:
            # tabela
            if len(df_bicsp) >= 1:
                # st.subheader(df_bicsp[escolha]["unidade"])
                tabela(
                    df_sunburst,
                    df_bicsp[escolha]["ano"],
                    df_bicsp[escolha]["nome"],
                )

    if st.session_state["opcao_visualizacao"] == "Sunburst + Sunburst":
        with col_filter_3:
            escolha_2 = st.selectbox(
                "Escolha o 2ºs dados para análise", df_bicsp, index=1
            )

        df_sunburst_2 = merge_portaria_bicsp(
            df_bicsp[escolha_2]["data"],
            df_bicsp[escolha_2]["ano"],
        )

        # metrica IDE 2
        with col_filter_4:
            st.metric(
                "IDE 2º",
                df_sunburst_2.loc[df_sunburst_2["Nome"] == "IDE", "Resultado"]
                .values[0]
                .round(1),
            )

        col_sun_1, col_sun_2 = st.columns(2)

        with col_sun_1:
            sunburst_bicsp(
                df_sunburst,
                df_bicsp[escolha]["ano"],
                df_bicsp[escolha]["mes"],
                df_bicsp[escolha]["unidade"],
                500,
            )

        with col_sun_2:
            sunburst_bicsp(
                df_sunburst_2,
                df_bicsp[escolha_2]["ano"],
                df_bicsp[escolha_2]["mes"],
                df_bicsp[escolha_2]["unidade"],
                500,
            )

    if st.session_state["opcao_visualizacao"] == "Dumbbell":
        if len(df_bicsp) == 1:
            dumbbell_plot(
                {df_bicsp[escolha]["nome"]: df_sunburst},
                df_bicsp[escolha]["ano"],
            )
        elif len(df_bicsp) > 1:
            with col_filter_3:
                escolha_2 = st.selectbox("Escolha o 2º gráfico", df_bicsp, index=1)

            df_sunburst_2 = merge_portaria_bicsp(
                df_bicsp[escolha_2]["data"],
                df_bicsp[escolha_2]["ano"],
            )

            # metrica IDE 2
            with col_filter_4:
                st.metric(
                    "IDE nº2",
                    df_sunburst_2.loc[df_sunburst_2["Nome"] == "IDE", "Resultado"]
                    .values[0]
                    .round(1),
                )

            dumbbell_plot(
                {
                    df_bicsp[escolha]["nome"]: df_sunburst,
                    df_bicsp[escolha_2]["nome"]: df_sunburst_2,
                },
                df_bicsp[escolha]["ano"],
            )
        st.write(
            """Interpretação/dicas:
- Se passares o rato por cima do círculo/quadrado mostra mais informação sobre o indicador.
- O tamanho do círculo/quadrado representa o peso do indicador - indicadores com mais impacto do IDE serão representados com um tamanho maior.
- A cor representa o score do indicador, entre 0-2 num gradiente vermelho -> amarelo -> verde.
- Quando é introduzido uma segundo ficheiro xlsx, é calculada a diferença entre os dois periodos para permitir avaliar a evolução temporal. Automaticamente o dados mais antigos serão círculos e o mais recente quadrados (mesmo que em cima fique trocado). Fica ordenado pelos dados antigos dos indicadores com pior para melhor score.
- A linha representa a variação do indicador entre os dois periodos, quando a diferença é significativa aparece a seta a indicar a direção da variação.
- Se o indicador se mantiver no mesmo valor, o circulo e o quadrado ficam sobrepostos.
- Para visualizar com mais detalhe, clica no botão de ecrã inteiro no canto superior direito do gráfico para aumentar o tamanho.
"""
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
            horizontal=True,
        )

    st.divider()

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


# @st.cache_data
def tab_visao_profissional(df_mimuf):
    col_filtro_medico_1, col_filtro_medico_2 = st.columns(2)

    with col_filtro_medico_1:
        dataframe_selected = st.selectbox(
            "Escolha o dataframe",
            df_mimuf,
        )

    with col_filtro_medico_2:
        filtro_medico = st.selectbox(
            "Médico Familia",
            (df_mimuf[dataframe_selected]["df"]["Médico Familia"].unique()),
        )

    sunburst_mimuf(
        df_mimuf[dataframe_selected]["df"][
            df_mimuf[dataframe_selected]["df"]["Médico Familia"] == filtro_medico
        ],
        df_mimuf[dataframe_selected]["ano"],
        df_mimuf[dataframe_selected]["mes"],
        df_mimuf[dataframe_selected]["unidade"],
        800,
    )
