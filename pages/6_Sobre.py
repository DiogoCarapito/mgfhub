import streamlit as st
import pandas as pd
from utils.style import (
    page_config,
    web_link,
    main_title,
    changelog_card,
    centered_title,
    centered_text,
    gradient_text,
    outros_projetos_card,
)

page_config()

main_title("Sobre")
st.write("")

# open content/socials.csv and read the content with pandas
socials = pd.read_csv("content/socials.csv")

# open content/sobre_o_projeto.txt
sobre_o_projeto = open("content/sobre_o_projeto.md", "r", encoding="utf-8").read()

# open content/changelog.csv and read the content with pandas
changelog = pd.read_csv("content/changelog.csv")

# order changelog by date, from the most recent to the oldest
changelog = changelog.sort_values(by="date", ascending=False)

# open content/outros_projetos.csv and read the content with pandas
outros_projetos = pd.read_csv("content/outros_projetos.csv")

centered_text(sobre_o_projeto)

st.divider()

centered_title("Sociais")

col_socials_1, col_socials_2 = st.columns([1, 1])
with col_socials_1:
    gradient_text("Diogo Carapito")
    for each in socials.values:
        web_link(each[0], each[1], each[2])

with col_socials_2:
    st.empty()

st.divider()

centered_title("Outros Projetos")

for each in outros_projetos.values:
    outros_projetos_card(each[0], each[1], each[2])


st.divider()

centered_title("Changelog")
st.write("")
st.write("")

for each in changelog.values:
    changelog_card(each[0], each[1], each[2])
