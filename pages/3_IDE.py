import streamlit as st
from utils.style import (
    page_config,
    main_title,
    em_desenvolvimento,
    # centered_title,
    # bicsp_link_page,
)

from utils.tutorial import tutorial_bicsp, tutorial_mimuf

from utils.etl_relatorios import etl_bicsp, etl_mimuf, merge_portaria_bicsp
from utils.vis_relatorios import (
    sunburst_bicsp,
    horizontal_bar_chart,
    # dumbbell_plot,
)


page_config()

main_title("IDE")

st.session_state["df_bicsp"] = {}
st.session_state["df_mimuf"] = {}
bicsp_nao_carregado = "Ficheiros do BI-CSP não carregados!"
mimuf_nao_carregado = "Ficheiros do MIM@UF não carregados!"


with st.sidebar:
    # upload de xlsx de bicsp
    st.markdown(
        "## Upload do Excel proveniente do [BI-CSP](https://bicsp.min-saude.pt/pt/contratualizacao/idg/Paginas/default.aspx)"
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
        "**Nota:** Para analise comparativa, pode carregar mais do que um ficheiro do BI-CSP de periodos diferentes"
    )

    tutorial_bicsp()

    st.divider()

    # bicsp_link_page()

    st.markdown("## Upload do Excel proveniente do MIMUF")

    # Upload de ficheiro excel do MIMUF
    st.session_state["uploaded_file_mimuf"] = st.file_uploader(
        "Upload excel proveniente do MIM@UF",
        type=["xlsx"],
        # help="Ajuda MIMUF",
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    tutorial_mimuf()


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
tab_uni_geral, tab_prof_geral = st.tabs(
    [
        "Unidade",
        # "Unidade - Indicadores",
        "Por profissional",
        # "Profissional - Indicadores",
        # "Todos Indicadores",
    ],
)

with tab_uni_geral:
    # centered_title("Unidade - Visão Geral")

    # mensagem se não houver ficheiros carregados
    if not st.session_state["df_bicsp"]:
        st.warning(bicsp_nao_carregado)

    else:
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

        if len(st.session_state["df_bicsp"]) > 1:
            # escolha do dataframe de analise 2
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

        if len(st.session_state["df_bicsp"]) == 1:
            sunburst_bicsp(
                df_sunburst,
                st.session_state["df_bicsp"][escolha]["ano"],
                st.session_state["df_bicsp"][escolha]["mes"],
                st.session_state["df_bicsp"][escolha]["unidade"],
                800,
            )

        elif len(st.session_state["df_bicsp"]) > 1:
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

        if len(st.session_state["df_bicsp"]) >= 1:
            horizontal_bar_chart(
                df_sunburst,
                st.session_state["df_bicsp"][escolha]["ano"],
            )

            # dumbbell_plot_single()
            # dumbbell_plot_double()


# with tab_uni_indic:
#     # centered_title("Unidade - Indicadores")

#     # mensagem se não houver ficheiros carregados
#     if not st.session_state["df_bicsp"]:
#         st.warning(bicsp_nao_carregado)

#     else:
#         st.write(st.session_state["df_bicsp"])

#     em_desenvolvimento()

with tab_prof_geral:
    # centered_title("Profissional - Visão Geral")

    if not st.session_state["df_mimuf"]:
        st.warning(mimuf_nao_carregado)

    elif len(st.session_state["df_mimuf"]) >= 1:
        for each in st.session_state["df_mimuf"].items():
            st.dataframe(each)

    else:
        pass

    em_desenvolvimento()

# with tab_prof_indi:
#     # centered_title("Profissional - Indicadores")


#     em_desenvolvimento()
