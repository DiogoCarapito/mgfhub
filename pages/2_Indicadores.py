import streamlit as st
import pandas as pd
from utils.utils import data_source
from utils.utils import filter_df

st.title("Indicadores")

# user interface
col1, col2 = st.columns([3, 1])

with col1:
    # campo de pesquisa
    pesquisa = st.text_input(
        "Pesquisa",
        "",
        # help="Pesquisa por nome, código ou conjunto de palavras"
    )

with col2:
    # radio de filtros
    filtros = st.radio(
        "Filtros",
        ["IDE", "IDG", "Todos"],
        index=2,
        horizontal=True,
        # help="Filtrar por tipo de indicadores"
    )


df = data_source("indicadores_sdm.csv")


filtered_df = filter_df(df, pesquisa, filtros)

num_indicatores = len(filtered_df)

# Numero de indicadores
st.metric("Número de Indicadores", num_indicatores)

# data display
table, cards = st.tabs(["Tabela", "Cartões"])

with table:
    # dataframe
    st.dataframe(filtered_df)

with cards:
    # loop over all rows in df
    for index, row in df.iterrows():
        st.write(row.iloc[0])
