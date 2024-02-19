import streamlit as st
from utils.style import page_config, main_title, em_desenvolvimento, centered_title

from utils.etl_relatorios import etl_bicsp, merge_portaria_bicsp
from utils.vis_relatorios import (
    sunburst_bicsp,
    horizontal_bar_chart,
    horizontal_bar_chart_2,
)

page_config()

main_title("Relatórios")

st.session_state["df_bicsp"] = {}
st.session_state["df_mimuf"] = {}


with st.sidebar:
    st.title("📄 Upload")

    # upload de xlsx de bicsp
    st.subheader("Upload excel proveniente do BI-CSP")

    # Upload de ficheiro excel do BI-CSP
    st.session_state["uploaded_file_bicsp"] = st.file_uploader(
        "Upload excel proveniente do BI-CSP",
        type=["xlsx"],
        # help="Ajuda BI-CSP",
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    st.subheader("Upload excel proveniente do MIMUF")

    # Upload de ficheiro excel do MIMUF
    st.session_state["uploaded_file_mimuf"] = st.file_uploader(
        "Upload excel proveniente do MIM@UF",
        type=["xlsx"],
        # help="Ajuda MIMUF",
        label_visibility="collapsed",
        accept_multiple_files=True,
    )

    st.divider()

    st.title("ℹ️ Ajuda")

    with st.expander(
        "Como extrair o ficheiro excel necessário do BI-CSP?", expanded=False
    ):
        st.write(
            "#### 1. Abrir o o [BI CSP](https://bicsp.min-saude.pt/pt/biselfservice/Paginas/home.aspx) e fazer login com as credenciais da ARS"
        )

        st.write(
            "#### 2. Ir ao separador dos **Indicadores | IDG** e selecionar o **IDG das Unidades Funcioinais**"
        )
        st.image("assets/tutorial/tutorial_bicsp_1.png", use_column_width=True)

        st.write("#### 3. Selecionar o separador **UF - IDG - Indicadores**")
        st.image("assets/tutorial/tutorial_bicsp_2.png", use_column_width=True)

        st.write("#### 4. Selecionar o **Mês** e a **Nome Unidade**")
        st.image("assets/tutorial/tutorial_bicsp_3.png", use_column_width=True)

        st.write(
            "#### 5. Selecionar o botão **More Options** no canto superior direito da tabela pirncipal"
        )
        st.image("assets/tutorial/tutorial_bicsp_4.png", use_column_width=True)

        st.write("#### 6. Selecionar primeira opção **Export data**")
        st.image("assets/tutorial/tutorial_bicsp_5.png", use_column_width=True)

        st.write(
            "#### 7. Selecionar a 3ª opção **Underlying data** e selecionar o botão **Export**"
        )
        st.image("assets/tutorial/tutorial_bicsp_6.png", use_column_width=True)

        st.write(
            "#### 8. Fazert o uload do ficheiro excel gerado (pasta de transferencias) neste site no local destinado a upload"
        )
        st.image("assets/tutorial/tutorial_bicsp_7.png", use_column_width=True)


# BICSP file
# if there is a file or files uploaded, process it/them
if st.session_state["uploaded_file_bicsp"] is not None:
    st.session_state["df_bicsp"] = etl_bicsp(st.session_state["uploaded_file_bicsp"])

# if empty
else:
    st.warning("<-- Ficheiro BI-CSP não carregado")
    st.empty()

# MIMUF file
# if there is a file or files uploaded, process it/them
if st.session_state["uploaded_file_mimuf"] is not None:
    st.session_state["df_mimuf"] = etl_bicsp(st.session_state["uploaded_file_mimuf"])

# if empty
else:
    st.warning("<-- Ficheiro MIM@UF não carregado")
    st.empty()

# select modelo contratual
# modelo_contratual = st.radio(
#     "Modelo Contratual",
#     ["IDE", "IDG", "Todos os indicadores"],
#     horizontal=True,
# )

tab_uni_geral, tab_uni_indic, tab_prof_geral, tab_prof_indi = st.tabs(
    [
        "Unidade - Geral",
        "Unidade - Indicadores",
        "Profissional - Geral",
        "Profissional - Indicadores",
    ],
)

with tab_uni_geral:
    centered_title("Unidade - Visão Geral")

    # mensagem se não houver ficheiros carregados
    if not st.session_state["df_bicsp"]:
        st.warning("Ficheiros do BI-CSP não carregados")

    else:
        col_filter_1, col_filter_2, col_filter_3, col_filter_4 = st.columns(
            [2, 1, 2, 1]
        )

        with col_filter_1:
            escolha = st.selectbox(
                "Escolha o mês de análise", st.session_state["df_bicsp"]
            )

        df_sunburst = merge_portaria_bicsp(
            st.session_state["df_bicsp"][escolha]["data"],
            st.session_state["df_bicsp"][escolha]["ano"],
        )
        with col_filter_2:
            st.metric(
                "IDE",
                df_sunburst.loc[df_sunburst["Nome"] == "IDE", "Resultado"]
                .values[0]
                .round(1),
            )

        with col_filter_3:
            if len(st.session_state["df_bicsp"]) > 1:
                escolha_2 = st.selectbox(
                    "Escolha o 2º gráfico", st.session_state["df_bicsp"], index=1
                )

        if len(st.session_state["df_bicsp"]) == 1:
            sunburst_bicsp(
                df_sunburst, st.session_state["df_bicsp"][escolha]["ano"], 800
            )

        elif len(st.session_state["df_bicsp"]) > 1:
            col_sun_1, col_sun_2 = st.columns(2)

            with col_sun_1:
                sunburst_bicsp(
                    df_sunburst, st.session_state["df_bicsp"][escolha]["ano"], 500
                )

            df_sunburst_2 = merge_portaria_bicsp(
                st.session_state["df_bicsp"][escolha_2]["data"],
                st.session_state["df_bicsp"][escolha_2]["ano"],
            )

            with col_sun_2:
                sunburst_bicsp(
                    df_sunburst_2, st.session_state["df_bicsp"][escolha_2]["ano"], 500
                )
        if len(st.session_state["df_bicsp"]) > 1:
            with col_filter_4:
                st.metric(
                    "IDE 2º",
                    df_sunburst_2.loc[df_sunburst_2["Nome"] == "IDE", "Resultado"]
                    .values[0]
                    .round(1),
                )

        if len(st.session_state["df_bicsp"]) >= 1:
            horizontal_bar_chart(
                df_sunburst,
                st.session_state["df_bicsp"][escolha]["ano"],
            )

            horizontal_bar_chart_2(df_sunburst)


with tab_uni_indic:
    centered_title("Unidade - Indicadores")

    em_desenvolvimento()

with tab_prof_geral:
    centered_title("Profissional - Visão Geral")

    em_desenvolvimento()

with tab_prof_indi:
    centered_title("Profissional - Indicadores")

    em_desenvolvimento()
