import streamlit as st


def main():
    st.set_page_config(
        page_title="mgfhub 2.0",
        page_icon="assets/favicon.ico",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("mgfhub 2.0")
    st.divider()

    col_1, col_2 = st.columns(2)
    with col_1:
        with st.container():
            st.header("Indicadores")
            st.write("Aqui vai o texto de apresentação dos indicadores")
            # st.link_button("Pesquisa", "/indicadores")

    with col_2:
        with st.container():
            st.header("Sunburst")
            st.write("Aqui vai o texto de apresentação do sunburst")
            # st.link_button("Sunburst", "/3_Sunburst.py")

    st.divider()

    col_3, col_4 = st.columns(2)

    with col_3:
        with st.container():
            st.header("Relatório")
            st.write("Aqui vai o texto de apresentação do relatório")
            # st.link_button("Relatório", "/4_Relatório.py")

    with col_4:
        with st.container():
            st.header("FAQs")
            st.write("Aqui vai o texto de apresentação do FAQs")
            # st.link_button("FAQs", "/5_FAQ.py")

    st.divider()


if __name__ == "__main__":
    main()
