import streamlit as st
import pandas as pd

from utils.style import (
    main_title,
    intro,
    card_container,
    double_space,
    # sidebar_about,
    page_config,
)


def main():
    page_config()

    # sidebar_about()

    # open content/cartoes_home.csv and read the content with pandas
    cartoes_home = pd.read_csv("content/cartoes_home.csv")

    # main title
    main_title("mgfhub")
    double_space()

    # style columns
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.empty()

    with col2:
        # introduction
        intro("Bem vind@ à nova versão 2.0 🎉")

        intro(
            "O mgfhub é uma plataforma de acesso aberto que disponibiliza informação e relatórios automáticos sobre os indicadores de monitorização dos Cuidados de Saúde Primários Portugueses."
        )

        double_space()

        for each in cartoes_home.values:
            card_container(
                title=each[0],
                text=each[1],
                image=None,
                link=each[3],
                # icon=each[4],
                em_construcao=each[5],
            )
            double_space()

    with col3:
        st.empty()


if __name__ == "__main__":
    main()
