import streamlit as st
import pandas as pd

from utils.style import (
    main_title,
    intro,
    card_container,
    page_config,
    bem_vindos_2,
    novidade,
)


def main():
    page_config()

    # open intro.md and read the content
    with open("content/intro.md", "r", encoding="utf-8") as file:
        indroducao = file.read()

    # open content/novidades.csv and pick the most recent one from date column
    ultima_novidade = (
        pd.read_csv("content/novidades.csv")
        .sort_values("date", ascending=False)
        .head(1)["text"]
        .values[0]
    )

    # open content/cartoes_home.csv and read the content with pandas
    cartoes_home = pd.read_csv("content/cartoes_home.csv")

    # main title
    main_title("mgfhub")

    # style columns
    col1, col2, col3 = st.columns([1, 6, 1])
    with col1:
        st.empty()

    with col2:
        # introduction
        bem_vindos_2("Bem vind@ à nova versão 2.1.0 🎉")

        intro(indroducao)

        novidade(ultima_novidade)

        for each in cartoes_home.values:
            card_container(
                title=each[0],
                text=each[1],
                image=None,
                link=each[3],
                # icon=each[4],
                em_construcao=each[5],
            )

    with col3:
        st.empty()


if __name__ == "__main__":
    main()
