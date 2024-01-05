import streamlit as st
import pandas as pd


st.title("Indicadores")

#URL de origem de dados
url = "https://github.com/DiogoCarapito/datasets_indicadores/raw/main/datasets/indicadores_sdm.csv"

#passa os dados para um pandas dataframe
df = pd.read_csv(url, index_col=0)


# campo de pesquisa
pesquisa = st.text_input("Pesquisa", "", help="Pesquisa por nome, código ou conjunto de palavras")


filtros, metrica = st.columns(2)

#filtros
with filtros:
    st.radio(
        "Filtros",
        ["IDE", "IDG", "Todos"],
        horizontal=True
    )

#Numero de indicadores
with metrica:
    st.metric(
        "Numero de Indicadores",
        "481"
    )

#dataframe
st.dataframe(df.head(10))    


