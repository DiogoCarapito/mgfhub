import streamlit as st
from utils.style import page_config, main_title, em_desenvolvimento

# imports that came from mgfhub2 project
# from utils.etl import etl_bicsp
# from utils.calc import calcular_idg, calcular_idg_maximo

page_config()

main_title("Relatórios")

em_desenvolvimento()

with st.sidebar:
    st.title("📄 Upload")

    # upload de xlsx de bicsp
    st.subheader("Upload excel proveniente do BI-CSP")
    st.session_state["uploaded_file_bicsp"] = st.file_uploader(
        "Upload excel proveniente do BI-CSP",
        type=["xlsx"],
        accept_multiple_files=False,
        # help="Ajuda BI-CSP",
        label_visibility="collapsed",
    )

    # upload de xlsx de mimuf

    st.subheader("Upload excel proveniente do MIMUF")

    st.session_state["uploaded_file_mimuf"] = st.file_uploader(
        "Upload excel proveniente do MIM@UF",
        type=["xlsx"],
        accept_multiple_files=False,
        # help="Ajuda MIMUF",
        label_visibility="collapsed",
    )

    st.divider()

    st.title("ℹ️ Ajuda")

    with st.expander(
        "Como extrair o ficheiro excel necessário do BI-CSP?", expanded=False
    ):
        # col1, col2, col3 = st.columns([1, 3, 1])
        # with col1:
        #    pass
        # with col2:
        st.write(
            "#### 1. Abrir o o [BI CSP](https://bicsp.min-saude.pt/pt/biselfservice/Paginas/home.aspx) e fazer login com as credenciais da ARS"
        )
        # st.divider()

        st.write(
            "#### 2. Ir ao separador dos **Indicadores | IDG** e selecionar o **IDG das Unidades Funcioinais**"
        )
        st.image("assets/tutorial/tutorial_bicsp_1.png", use_column_width=True)
        # st.divider()

        st.write("#### 3. Selecionar o separador **UF - IDG - Indicadores**")
        st.image("assets/tutorial/tutorial_bicsp_2.png", use_column_width=True)
        # st.divider()

        st.write("#### 4. Selecionar o **Mês** e a **Nome Unidade**")
        st.image("assets/tutorial/tutorial_bicsp_3.png", use_column_width=True)
        # st.divider()

        st.write(
            "#### 5. Selecionar o botão **More Options** no canto superior direito da tabela pirncipal"
        )
        st.image("assets/tutorial/tutorial_bicsp_4.png", use_column_width=True)
        # st.divider()

        st.write("#### 6. Selecionar primeira opção **Export data**")
        st.image("assets/tutorial/tutorial_bicsp_5.png", use_column_width=True)
        # st.divider()

        st.write(
            "#### 7. Selecionar a 3ª opção **Underlying data** e selecionar o botão **Export**"
        )
        st.image("assets/tutorial/tutorial_bicsp_6.png", use_column_width=True)
        # st.divider()

        st.write(
            "#### 8. Fazert o uload do ficheiro excel gerado (pasta de transferencias) neste site no local destinado a upload"
        )
        st.image("assets/tutorial/tutorial_bicsp_7.png", use_column_width=True)
    # with col3:
    #    pass


# sidebar_about()


if st.session_state["uploaded_file_bicsp"] is None:
    st.warning("Nenhum ficheiro carregado")

else:
    st.write(st.session_state["uploaded_file_bicsp"])
