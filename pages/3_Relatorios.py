import streamlit as st
from utils.style import page_config, main_title, em_desenvolvimento, centered_title
import pandas as pd

from utils.etl_relatorios import etl_bicsp
from utils.vis_relatorios import sunburst_bicsp

# imports that came from mgfhub2 project
# from utils.etl import etl_bicsp
# from utils.calc import calcular_idg, calcular_idg_maximo

page_config()

main_title("Relatórios")

st.session_state["df_bicsp"] = None
st.session_state["df_mimuf"] = None

with st.sidebar:
    st.title("📄 Upload")

    # upload de xlsx de bicsp
    st.subheader("Upload excel proveniente do BI-CSP")

    # Upload de ficheiro excel do BI-CSP
    st.session_state["uploaded_file_bicsp"] = st.file_uploader(
        "Upload excel proveniente do BI-CSP",
        type=["xlsx"],
        accept_multiple_files=False,
        # help="Ajuda BI-CSP",
        label_visibility="collapsed",
    )

    st.subheader("Upload excel proveniente do MIMUF")

    # Upload de ficheiro excel do MIMUF
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
if st.session_state["uploaded_file_bicsp"] is not None:
    st.session_state["df_bicsp"] = etl_bicsp(
        pd.read_excel(st.session_state["uploaded_file_bicsp"], engine="openpyxl")
    )
    # st.write(df_bicsp)

else:
    st.warning("Ficheiro BI-CSP não carregado")
    st.empty()

# MIMUF file
if st.session_state["uploaded_file_mimuf"] is not None:
    st.session_state["df_mimuf"] = etl_bicsp(
        pd.read_excel(st.session_state["uploaded_file_mimuf"], engine="openpyxl")
    )
    # st.write(df_mimuf)

else:
    st.warning("Ficheiro MIM@UF não carregado")
    st.empty()


modelo_contratual = st.radio(
    "Modelo Contratual",
    [
        "IDE",
        "IDG",
    ],
    horizontal=True,
)

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

    col_uni_geral_1, col_uni_geral_2 = st.columns([2, 1])
    with col_uni_geral_1:
        # sunburst
        st.plotly_chart(
            sunburst_bicsp(st.session_state["df_bicsp"]), use_container_width=True
        )

    with col_uni_geral_2:
        st.metric(modelo_contratual, 100)

    st.write("texto")

with tab_uni_indic:
    centered_title("Unidade - Indicadores")

with tab_prof_geral:
    centered_title("Profissional - Visão Geral")

with tab_prof_indi:
    centered_title("Profissional - Indicadores")


em_desenvolvimento()
