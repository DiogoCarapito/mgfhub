import streamlit as st
from utils.etl_relatorios import etl_bicsp, etl_mimuf


# Sidebar with uplods of xlsx files
def ide_sidebar():
    with st.sidebar:
        # upload de xlsx de bicsp

        # st.warning(
        #     "Ainda não é possível fazer upload de ficheiros do BI-CSP e MIM@UF referentes ao ano de 2025. Será corrigido até ao fim de Março."
        # )

        # st.success(
        #     "Já é possivel analisar dados de 2025! Se encontrar algum erro agradeço o contacto pelo endereço de email mgfhub.suporte@gmail.com"
        # )

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
            '(Também é possível extrair o ficheiro do BI-CSP na nova secção do [IDE](https://bicsp.min-saude.pt/pt/contratualizacao/ide/Paginas/default.aspx), separador "Dimensões e Indicadores IDE")'
        )

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
