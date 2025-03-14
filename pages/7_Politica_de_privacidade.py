import streamlit as st
from utils.style import (
    mgfhub_style,
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

main_title("Politica de Privacidade")

# read the terms of use from content/politica_privacidade.md
with open("content/politica_privacidade.md", "r") as file:
    politica_privacidade = file.read()

st.markdown(politica_privacidade)

bottom_suport_email()
