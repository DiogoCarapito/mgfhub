import pandas as pd
import os
import streamlit as st


def func():
    return None


def data_source(source):
    # check if source is in ./data folder
    # if not, download from github

    data_files_list = os.listdir("./data")

    if source in data_files_list:
        return pd.read_csv("./data/" + source, index_col=0)

    else:
        url = "https://github.com/DiogoCarapito/datasets_indicadores/raw/main/datasets/indicadores_sdm.csv"
        return pd.read_csv(url, index_col=0)


def upsave_data_source(source):
    url = "https://github.com/DiogoCarapito/datasets_indicadores/raw/main/datasets/indicadores_sdm.csv"
    df = pd.read_csv(url, index_col=0)
    df.to_csv("./data/" + source)
    print(f"{source} saved successfully!")


def button_link(label):
    st.markdown(
        f'<a href={label} target="_self">'
        f'<button style="color: white; background-color: #0000F5; border: none; cursor: pointer; '
        f"padding: 10px 24px; text-align: center; text-decoration: none; display: inline-block; "
        f"border-radius: 8px; -webkit-border-radius: 8px; -moz-border-radius: 8px; "
        f'font-size: 16px; margin: 4px 2px; -webkit-transition-duration: 0.4s; transition-duration: 0.4s;">'
        f"Ir para {label}"
        f"</button></a>",
        unsafe_allow_html=True,
    )


def web_link(label, link, icon):
    st.markdown(
        f'<a href={link} target="_self">'
        f'<img src={icon} alt="linkedin" width="16" height="16">'
        f"{label}"
        f"</a>",
        unsafe_allow_html=True,
    )
