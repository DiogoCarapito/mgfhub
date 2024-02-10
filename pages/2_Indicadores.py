import streamlit as st
from utils.utils import data_source, filter_df
from utils.style import main_title, cartao_indicador

main_title("Indicadores")

# user interface
col_pesquisa_1, col_pesquisa_2 = st.columns([5, 1])

with col_pesquisa_1:
    # campo de pesquisa
    pesquisa = st.text_input(
        label="Pesquisa",
        value="",
        label_visibility="collapsed",
        help="Pesquisa por nome, código ou conjunto de palavras",
    )

with col_pesquisa_2:
    st.button("Pesquisar", disabled=True)

# radio de filtros
filtros = st.radio(
    "Filtros",
    ["IDE", "IDG", "Todos"],
    index=0,
    horizontal=True,
    # help="Filtrar por tipo de indicadores",
)


df = data_source("indicadores_sdm_complete.csv")


filtered_df = filter_df(df, pesquisa, filtros)

showable_df = filtered_df.drop(
    columns=["search_indexes", "ide", "idg", "Área | Subárea | Dimensão"]
)
# showable_df = filtered_df.drop(columns=["ide", "idg", "Área | Subárea | Dimensão"])
# showable_df.set_index("id", inplace=True)

num_indicatores = len(filtered_df)

# Numero de indicadores
st.metric("Número de Indicadores", num_indicatores)

# data display
# cards, table = st.tabs(["Cartões", "Tabela"])
table, cards = st.tabs(["Tabela", "Cartões"])

with table:
    # dataframe
    st.dataframe(
        showable_df,
        column_config={
            "link_sdm": st.column_config.LinkColumn(
                label="Link",
                display_text="SDM",
            )
        },
        use_container_width=False,
        hide_index=True,
        column_order=[
            "id",
            "link_sdm",
            "Designação",
            "Área clínica",
            "Intervalo Aceitável",
            "Intervalo Esperado",
        ],
    )


with cards:
    # loop over all rows in df
    for index, row in filtered_df.iterrows():
        # cartao_indicador(index, row.to_dict())
        cartao_indicador(index, row.to_dict())
