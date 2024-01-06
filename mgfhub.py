import streamlit as st
from utils.components import button_link
from utils.style import main_title


def main():
    st.set_page_config(
        page_title="mgfhub",
        page_icon="assets/favicon.ico",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    main_title("mgfhub")

    st.markdown("")
    st.markdown("")

    st.markdown(
        "##### O mgfhub é uma plataforma de acesso aberto que disponibiliza informação sobre os indicadores de monitorização e avaliação dos Cuidados de Saúde Primários Portugueses."
    )

    st.markdown("")
    st.markdown("")

    col_1, col_2 = st.columns(2)
    with col_1:
        with st.container():
            st.header("Indicadores")
            st.write("Aqui vai o texto de apresentação dos indicadores")
            # st.image("assets/indicadores.png")
            button_link("Indicadores")

    with col_2:
        with st.container():
            st.header("Sunburst")
            st.write("Aqui vai o texto de apresentação do sunburst")
            button_link("Sunburst")

    st.markdown("")
    st.markdown("")

    col_3, col_4 = st.columns(2)

    with col_3:
        with st.container():
            st.header("Relatórios")
            st.write("Aqui vai o texto de apresentação do relatório")
            button_link("Relatórios")

    with col_4:
        with st.container():
            st.header("FAQs")
            st.write("Aqui vai o texto de apresentação do FAQs")
            button_link("FAQs")


if __name__ == "__main__":
    main()
