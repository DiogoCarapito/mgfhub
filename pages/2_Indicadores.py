import streamlit as st
import pandas as pd
from utils.utils import data_source

st.title("Indicadores")


df = data_source("indicadores_sdm.csv")


# campo de pesquisa
pesquisa = st.text_input(
    "Pesquisa", "", help="Pesquisa por nome, código ou conjunto de palavras"
)


filtros, metrica = st.columns(2)

# filtros
with filtros:
    st.radio("Filtros", ["IDE", "IDG", "Todos"], horizontal=True)

# Numero de indicadores
with metrica:
    st.metric("Numero de Indicadores", "481")

# dataframe
st.dataframe(df.head(10))
