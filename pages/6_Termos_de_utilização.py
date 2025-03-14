import streamlit as st
from utils.style import (
    page_config,
    # web_link,
    main_title,
    # changelog_card,
    # centered_title,
    # centered_text,
    # gradient_text,
    # outros_projetos_card,
    bottom_suport_email,
    # em_desenvolvimento,
)

page_config()

main_title("Termos de utilização")

# read the terms of use from /content/termos_de_utilizacao.md
with open("content/termos_utilização.md", "r") as file:
    termos_de_utilizacao = file.read()

st.markdown(termos_de_utilizacao)

bottom_suport_email()
