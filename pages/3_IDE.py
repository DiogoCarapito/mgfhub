import streamlit as st
from utils.style import (
    page_config,
    main_title,
    # em_desenvolvimento,
    # centered_title,
    # bicsp_link_page,
)


from utils.etl_relatorios import etl_bicsp, etl_mimuf, merge_portaria_bicsp
from utils.vis_relatorios import (
    sunburst_bicsp,
    dumbbell_plot,
    tabela,
    horizontal_bar,
    sunburst_mimuf,
    # stakced_barchart,
)


page_config()

main_title("IDE")

st.session_state["df_bicsp"] = {}
st.session_state["df_mimuf"] = {}
bicsp_nao_carregado = "Ficheiros do BI-CSP não carregados!"
mimuf_nao_carregado = "Ficheiros do MIM@UF não carregados!"
st.session_state["opcao_visualizacao"] = "Sunburst"
st.session_state["opcao_visualizacao_2"] = "Barras + Tabela"


with st.sidebar:
    # upload de xlsx de bicsp
    st.markdown(
        "## Upload do excel do [BI-CSP](https://bicsp.min-saude.pt/pt/contratualizacao/idg/Paginas/default.aspx)"
    )

    # Upload de ficheiro excel do BI-CSP
    st.session_state["uploaded_file_bicsp"] = st.file_uploader(
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

    # bicsp_link_page()

    st.markdown("## Upload do excel do MIMUF")

    # Upload de ficheiro excel do MIMUF
    st.session_state["uploaded_file_mimuf"] = st.file_uploader(
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

    # st.write("")
    st.markdown(
        "**Nota:** Podes carregar mais do que um ficheiro do BI-CSP e/ou MIM@UF com periodos diferentes. permite comparar diferentes periodos e/ou unidades."
    )


# BICSP file
st.session_state["df_bicsp"] = etl_bicsp(st.session_state["uploaded_file_bicsp"])

# MIMUF file
st.session_state["df_mimuf"] = etl_mimuf(st.session_state["uploaded_file_mimuf"])

# Seleção modelo contratual
# modelo_contratual = st.radio(
#     "Modelo Contratual",
#     ["IDE", "IDG", "Todos os indicadores"],
#     horizontal=True,
# )

# tab_uni_geral, tab_uni_indic, tab_prof_geral, tab_prof_indi = st.tabs(
tab_uni_geral, tab_equipas, tab_prof_geral = st.tabs(
    [
        "Visão de Unidade",
        "Visão de Equipas",
        "Visão por Profissional",
        # "Profissional - Indicadores",
        # "Todos Indicadores",
    ],
)

with tab_uni_geral:
    # centered_title("Unidade - Visão Geral")

    # mensagem se não houver ficheiros carregados
    if not st.session_state["df_bicsp"]:
        st.warning(bicsp_nao_carregado)

        st.write("")

        # tutorial_bicsp()
        st.markdown(
            '<p style="text-align: center;">'
            '<a href="https://mgfhub.com/FAQs">Como extrair o ficheiro excel do BI-CSP?</a>'
            "</p>",
            unsafe_allow_html=True,
        )

    else:
        opções_visualizacao = (
            [
                "Sunburst",
                "Tabela",
                "Sunburst + Tabela",
                "Dumbbell",
                "Sunburst + Sunburst",
            ]
            if len(st.session_state["df_bicsp"]) > 1
            else ["Sunburst", "Tabela", "Sunburst + Tabela", "Dumbbell"]
        )
        # Dumbbell chart by default if more than one file uploaded
        index_visualizacao = 3 if len(st.session_state["df_bicsp"]) > 1 else 0

        st.session_state["opcao_visualizacao"] = st.radio(
            "Visualização",
            opções_visualizacao,
            horizontal=True,
            index=index_visualizacao,
            # label_visibility="collapsed",
            key="opcao_visualizacao_1",
        )

        st.divider()

        # filtros
        col_filter_1, col_filter_2, col_filter_3, col_filter_4 = st.columns(
            [2, 1, 2, 1]
        )

        # escolha do dataframe de analise
        with col_filter_1:
            escolha = st.selectbox(
                "Escolha o mês de análise", st.session_state["df_bicsp"]
            )
        # processamento do dataframe
        df_sunburst = merge_portaria_bicsp(
            st.session_state["df_bicsp"][escolha]["data"],
            st.session_state["df_bicsp"][escolha]["ano"],
        )

        # metrica IDE
        with col_filter_2:
            st.metric(
                "IDE",
                df_sunburst.loc[df_sunburst["Nome"] == "IDE", "Resultado"]
                .values[0]
                .round(1),
            )

        # SUNBURST
        if st.session_state["opcao_visualizacao"] == "Sunburst":
            # if len(st.session_state["df_bicsp"]) == 1:
            sunburst_bicsp(
                df_sunburst,
                st.session_state["df_bicsp"][escolha]["ano"],
                st.session_state["df_bicsp"][escolha]["mes"],
                st.session_state["df_bicsp"][escolha]["unidade"],
                800,
            )

        # TABELA
        if st.session_state["opcao_visualizacao"] == "Tabela":
            # tabela
            if len(st.session_state["df_bicsp"]) >= 1:
                # st.write(df_sunburst[["Nome", "Resultado", "Score"]])
                tabela(
                    df_sunburst,
                    st.session_state["df_bicsp"][escolha]["ano"],
                    st.session_state["df_bicsp"][escolha]["nome"],
                )
        # SUNBURST + TABELA
        if st.session_state["opcao_visualizacao"] == "Sunburst + Tabela":
            col_1, col_2 = st.columns([1, 1])
            with col_1:
                sunburst_bicsp(
                    df_sunburst,
                    st.session_state["df_bicsp"][escolha]["ano"],
                    st.session_state["df_bicsp"][escolha]["mes"],
                    st.session_state["df_bicsp"][escolha]["unidade"],
                    500,
                )
            with col_2:
                # tabela
                if len(st.session_state["df_bicsp"]) >= 1:
                    # st.subheader(st.session_state["df_bicsp"][escolha]["unidade"])
                    tabela(
                        df_sunburst,
                        st.session_state["df_bicsp"][escolha]["ano"],
                        st.session_state["df_bicsp"][escolha]["nome"],
                    )

        if st.session_state["opcao_visualizacao"] == "Sunburst + Sunburst":
            with col_filter_3:
                escolha_2 = st.selectbox(
                    "Escolha o 2º gráfico", st.session_state["df_bicsp"], index=1
                )

            df_sunburst_2 = merge_portaria_bicsp(
                st.session_state["df_bicsp"][escolha_2]["data"],
                st.session_state["df_bicsp"][escolha_2]["ano"],
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
                    st.session_state["df_bicsp"][escolha]["ano"],
                    st.session_state["df_bicsp"][escolha]["mes"],
                    st.session_state["df_bicsp"][escolha]["unidade"],
                    500,
                )

            with col_sun_2:
                sunburst_bicsp(
                    df_sunburst_2,
                    st.session_state["df_bicsp"][escolha_2]["ano"],
                    st.session_state["df_bicsp"][escolha_2]["mes"],
                    st.session_state["df_bicsp"][escolha_2]["unidade"],
                    500,
                )

        if st.session_state["opcao_visualizacao"] == "Dumbbell":
            if len(st.session_state["df_bicsp"]) == 1:
                dumbbell_plot(
                    {st.session_state["df_bicsp"][escolha]["nome"]: df_sunburst},
                    st.session_state["df_bicsp"][escolha]["ano"],
                )
            elif len(st.session_state["df_bicsp"]) > 1:
                with col_filter_3:
                    escolha_2 = st.selectbox(
                        "Escolha o 2º gráfico", st.session_state["df_bicsp"], index=1
                    )

                df_sunburst_2 = merge_portaria_bicsp(
                    st.session_state["df_bicsp"][escolha_2]["data"],
                    st.session_state["df_bicsp"][escolha_2]["ano"],
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
                        st.session_state["df_bicsp"][escolha]["nome"]: df_sunburst,
                        st.session_state["df_bicsp"][escolha_2]["nome"]: df_sunburst_2,
                    },
                    st.session_state["df_bicsp"][escolha]["ano"],
                )


with tab_equipas:
    if not st.session_state["df_mimuf"]:
        st.warning(mimuf_nao_carregado)
        st.write("")
        # tutorial_mimuf()
        st.markdown(
            '<p style="text-align: center;">'
            '<a href="https://mgfhub.com/FAQs">Como extrair o ficheiro excel do MIM@UF?</a>'
            "</p>",
            unsafe_allow_html=True,
        )

    else:
        # Visualizaçao

        # if len(st.session_state["df_mimuf"]) > 1:
        #     st.session_state["opcao_visualizacao_2"] = st.radio(
        #         "Visualização",
        #         ["Barras + Tabela", "Barras + Barras"],
        #         horizontal=True,
        #     )

        # st.divider()

        col_filtro_equipa_1, col_filtro_equipa_2, col_visualizacao = st.columns(
            [2, 2, 2]
        )
        with col_filtro_equipa_1:
            dataframe_selected = st.selectbox(
                "Escolha o mês de analise",
                st.session_state["df_mimuf"],
            )

        with col_filtro_equipa_2:
            lista_indicadores = st.session_state["df_mimuf"][dataframe_selected]["df"][
                "Nome"
            ].unique()
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
                st.session_state["df_mimuf"][dataframe_selected]["df"].loc[
                    st.session_state["df_mimuf"][dataframe_selected]["df"]["Nome"]
                    == filtro_indicador
                ],
                st.session_state["df_mimuf"][dataframe_selected]["ano"],
                st.session_state["opcao_visualizacao_2"],
            )

        with col_graph_2:
            # link for sdm by using th id of the indicador selected
            # extract the initial numbers inside this string
            filtro_indicador_id = filtro_indicador.split(" ")[0]
            link = f"https://sdm.min-saude.pt/BI.aspx?id={filtro_indicador_id}"
            text = f"link SDM indicador {filtro_indicador_id}"

            st.markdown(f"[{text}]({link})")

            st.dataframe(
                st.session_state["df_mimuf"][dataframe_selected]["df"]
                .loc[
                    st.session_state["df_mimuf"][dataframe_selected]["df"]["Nome"]
                    == filtro_indicador
                ][["Médico Familia", "Numerador", "Denominador", "Valor"]]
                .sort_values(
                    by=st.session_state["opcao_visualizacao_2"], ascending=False
                ),
                hide_index=True,
            )

        # stakced_barchart(
        #     st.session_state["df_mimuf"][dataframe_selected]["df"]
        #         .loc[
        #             st.session_state["df_mimuf"][dataframe_selected]["df"]["Nome"]
        #             == filtro_indicador
        #         ][["Médico Familia", "Numerador", "Denominador", "Valor"]]
        #         .sort_values(by="Numerador", ascending=False),
        #     )

# with tab_uni_indic:
#     # centered_title("Unidade - Indicadores")

#     # mensagem se não houver ficheiros carregados
#     if not st.session_state["df_bicsp"]:r
#         st.warning(bicsp_nao_carregado)

#     else:
#         st.write(st.session_state["df_bicsp"])

#     em_desenvolvimento()

with tab_prof_geral:
    # centered_title("Profissional - Visão Geral")

    if not st.session_state["df_mimuf"]:
        st.warning(mimuf_nao_carregado)
        st.write("")
        # tutorial_mimuf()
        st.markdown(
            '<p style="text-align: center;">'
            '<a href="https://mgfhub.com/FAQs">Como extrair o ficheiro excel do MIM@UF?</a>'
            "</p>",
            unsafe_allow_html=True,
        )

    elif len(st.session_state["df_mimuf"]) >= 1:
        # opções_visualizacao_2 = (
        #     [
        #         "Sunburst",
        #         "Tabela",
        #         "Sunburst + Tabela",
        #         "Dumbbell",
        #         "Sunburst + Sunburst",
        #     ]
        #     if len(st.session_state["df_mimuf"]) > 1
        #     else ["Sunburst", "Tabela", "Sunburst + Tabela", "Dumbbell"]
        # )
        # # Dumbbell chart by default if more than one file uploaded
        # index_visualizacao_2 = 3 if len(st.session_state["df_mimuf"]) > 1 else 0

        # st.session_state["opcao_visualizacao_2"] = st.radio(
        #     "Visualização",
        #     opções_visualizacao_2,
        #     horizontal=True,
        #     index=index_visualizacao_2,
        #     key="opcao_visualizacao_2",
        # )

        # st.divider()

        col_filtro_medico_1, col_filtro_medico_2 = st.columns(2)

        with col_filtro_medico_1:
            dataframe_selected = st.selectbox(
                "Escolha o dataframe",
                st.session_state["df_mimuf"],
            )

        with col_filtro_medico_2:
            filtro_medico = st.selectbox(
                "Médico Familia",
                (
                    st.session_state["df_mimuf"][dataframe_selected]["df"][
                        "Médico Familia"
                    ].unique()
                ),
            )

        sunburst_mimuf(
            st.session_state["df_mimuf"][dataframe_selected]["df"][
                st.session_state["df_mimuf"][dataframe_selected]["df"]["Médico Familia"]
                == filtro_medico
            ],
            st.session_state["df_mimuf"][dataframe_selected]["ano"],
            st.session_state["df_mimuf"][dataframe_selected]["mes"],
            st.session_state["df_mimuf"][dataframe_selected]["unidade"],
            800,
        )

        # for nome, each in st.session_state["df_mimuf"].items():
        #     sunburst_mimuf(
        #         each["df"][each["df"]["Médico Familia"] == filtro_medico],
        #         each["ano"],
        #         each["mes"],
        #         each["unidade"],
        #         500,
        #     )


# with tab_prof_indi:
#     # centered_title("Profissional - Indicadores")


#     em_desenvolvimento()
