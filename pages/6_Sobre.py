# import streamlit as st
from utils.style import web_link, main_title, sidebar_about

main_title("Sobre")

sidebar_about()


# link to gihub, personal website, twitter and linkedin
web_link(
    "diogocarapito.com",
    "https://diogocarapito.com/",
    "https://raw.githubusercontent.com/DiogoCarapito/blog/main/static/favicon.ico",
)

web_link(
    "Github",
    "https://github.com/DiogoCarapito",
    "https://icons.getbootstrap.com/assets/icons/github.svg",
)

web_link(
    "Twitter",
    "https://twitter.com/DiogoCarapito",
    "https://icons.getbootstrap.com/assets/icons/twitter-x.svg",
)

web_link(
    "LinkedIn",
    "https://www.linkedin.com/in/diogo-carapito-564a51262/",
    "https://icons.getbootstrap.com/assets/icons/linkedin.svg",
)
