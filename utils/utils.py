import pandas as pd
import os
from unidecode import unidecode
from rapidfuzz import process, fuzz
import streamlit as st


def func():
    return None


@st.cache_data
def data_source(source):
    # check if source is in ./data folder
    # if not, download from github
    data_files_list = os.listdir("./data")

    if source in data_files_list:
        return pd.read_csv("./data/" + source, index_col=0)

    else:
        url = "https://github.com/DiogoCarapito/datasets_indicadores/raw/main/datasets/indicadores_sdm.csv"

        df = pd.read_csv(url, index_col=0)

        return df


@st.cache_data
def filter_df(df, pesquisa, filtros, area_clinica):
    if filtros == "IDE":
        df = df[df["ide"] == 1]

    elif filtros == "IDG":
        df = df[df["idg"] == 1]

    elif filtros == "BI-CSP":
        df = df[df["bicsp"] == 1]

    else:
        pass

    if area_clinica:
        df = df[df["Área clínica"].isin(area_clinica)]

    pesquisa = unidecode(pesquisa.lower())

    if pesquisa == "":
        return df
    else:
        # fuzzy search com score cutoff de 59, comparando com indexing
        search_list = process.extract(
            pesquisa,
            df["search_indexes"],
            scorer=fuzz.WRatio,
            score_cutoff=59,
            limit=50,
        )
        df = df.filter([id[2] for id in search_list], axis=0)

        return df


@st.cache_data
def num_denom_paragraph(text):
    try:
        text_after_split = text.split("Numerador: ")
        text_after_split_2 = text_after_split[1].split("Denominador: ")
        text = [text_after_split[0], text_after_split_2[0], text_after_split_2[1]]
        return text
    except IndexError:
        return [text, "", ""]
