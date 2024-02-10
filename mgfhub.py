import streamlit as st

from utils.style import main_title, intro, card_container, double_space


def main():
    st.set_page_config(
        page_title="mgfhub",
        page_icon="assets/favicon.ico",
        layout="wide",
        initial_sidebar_state="auto",
    )

    # main title
    main_title("mgfhub")
    double_space()

    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.empty()

    with col2:
        # introduction
        intro(
            "O mgfhub é uma plataforma de acesso aberto que disponibiliza informação e relatórios automáticos sobre os indicadores de monitorização dos Cuidados de Saúde Primários Portugueses."
        )
        double_space()

        card_container(
            title="Indicadores",
            text="Ferramenta de pesquisa de indicadores, com possibilidade de filtrar por com impacto no IDE ou IDG.",
            image=None,
            link="pages/2_Indicadores.py",
            icon="🔎",
        )

        double_space()

        card_container(
            title="Sunburst",
            text="Visualização da distribuição dos indicadores pelo seu impacto no IDE e IDG. permite compreeender a distribuição dos indicadores pelas diferentes àreas e dimensões.",
            image=None,
            link="pages/3_Sunburst.py",
            icon="🌞",
        )
        double_space()

        card_container(
            title="Relatórios",
            text="Ferramenta de analise automatica da performance dos indicadores de uma unidade ou de um profissional, com base no upload de uma tabela proveniente do BI-CSP.",
            image=None,
            link="pages/4_Relatorios.py",
            icon="📊",
        )

        double_space()

        card_container(
            title="FAQs",
            text="Perguntas frequentes sobre o mgfhub, funcionamento dos indicadores e sua interpretação.",
            image=None,
            link="pages/5_FAQs.py",
            icon="❓",
        )

    with col3:
        st.empty()


if __name__ == "__main__":
    main()
