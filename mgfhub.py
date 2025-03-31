import streamlit as st
import pandas as pd

from utils.style import (
    main_title,
    intro,
    card_container,
    page_config,
    # bem_vindos_2,
    novidades,
    bottom_suport_email,
)

#from utils.grpd import consent_popup


def main():
    page_config()

    # main title
    main_title("mgfhub")

    # style columns
    col1, col2, col3 = st.columns([1, 6, 1])

    # empty column to style the page
    with col1:
        st.empty()

    # main content
    with col2:
        # welcome message
        # bem_vindos_2("Bem vind@ à nova versão 2.1 🎉")

        # intro from content/intro.md
        intro("content/intro.md")

        # novidades from content/novidades.csv
        # it picks the most recent one
        novidades("content/changelog.csv")
        
        st.warning("Ainda não é possível fazer upload de ficheiros do BI-CSP e MIM@UF referentes ao ano de 2025. Será corrigido até ao fim de Março.")

        # card containers with links to other pages

        # open content/cartoes_home.csv and read the content with pandas
        cartoes_home = pd.read_csv("content/cartoes_home.csv")

        # loop through the content and create a card for each row
        for each in cartoes_home.values:
            card_container(
                title=each[0],
                text=each[1],
                image=None,
                # link=each[3],
                # icon=each[4],
                em_construcao=each[5],
            )

    # empty column to style the page
    with col3:
        st.empty()

    # if "consent" not in st.session_state:
    #     consent_popup()

    st.write("")
    bottom_suport_email()


if __name__ == "__main__":
    main()
