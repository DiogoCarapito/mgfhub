import streamlit as st
from utils.utils import data_source, filter_df
from utils.style import page_config, main_title, cartao_indicador, bottom_suport_email

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# Configuração da página
page_config()

# titulo principal estilizado com a função main_title
main_title("Indicadores")

# Supabase configuration
# load .env file
load_dotenv()

# get Supabase URL and Key from environment variables
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# Function to insert data into Supabase
def supabase_insert(input_text, filtro):
    # Get current datetime
    date_time = datetime.now().isoformat()

    # Create the data in a format to be inserted into Supabase
    sb_insert = {"created_at": date_time, "query": input_text, "filter": filtro}

    # Insert data into Supabase
    supabase.table("mgfhub_queries").insert(sb_insert).execute()


# Variaveis iniciais
# carregar o dataframe com os indicadores
st.session_state["df"] = data_source("indicadores_sdm_complete.csv")

# campode pesquisa inicial
st.session_state["pesquisa"] = ""

# opções de filtros para o radio
radio_optioins = ["IDE", "IDG", "Todos"]

# opção de filtro inicial
st.session_state["filtros"] = radio_optioins[0]

# opção de filtro de área clínica -> nenhum
st.session_state["filtro_area_clinica"] = (
    st.session_state["df"]
    .loc[st.session_state["df"]["ide"] == 1, "Área clínica"]
    .unique()
    .tolist()
)


def update_dataframes(df, pesquisa, filtros, filtro_area_clinica):
    # filtragem do dataframe com base na pesquisa e nos filtros
    st.session_state["filtered_df"] = (
        # função para filtrar o dataframe com base na pesquisa e nos filtros
        filter_df(
            df,
            pesquisa,
            filtros,
            filtro_area_clinica,
        )
        # ordenar o dataframe pelo index
        .set_index("id")
        # ordenar o dataframe pelo index
        .sort_index()
    )

    # dataframe com os indicadores para visualização, filtrando as colunas que não são necessárias para a tabel
    st.session_state["showable_df"] = st.session_state["filtered_df"].drop(
        # columns=["search_indexes", "ide", "idg", "Área | Subárea | Dimensão"]
        columns=["ide", "idg", "Área | Subárea | Dimensão"]
    )


# update_dataframes(
#     st.session_state["df"],
#     st.session_state["pesquisa"],
#     st.session_state["filtros"],
#     st.session_state["filtro_area_clinica"]
# )


# função para executar a pesquisa, é chamada quando o botão de pesquisa é clicado ou quando a página é aberta
# (mesmo quando o Enter é clicado no st.text_input)
def on_click():
    # atualizar os dataframes com base na pesquisa e nos filtros
    update_dataframes(
        st.session_state["df"],
        st.session_state["pesquisa"],
        st.session_state["filtros"],
        st.session_state["filtro_area_clinica"],
    )

    # log the search to supabase
    supabase_insert(st.session_state["pesquisa"], st.session_state["filtros"])


# user interface
# col_pesquisa_1, col_pesquisa_2 = st.columns([5, 1])
col_pesquisa_1, col_pesquisa_2 = st.columns([11, 1])

with col_pesquisa_1:
    # campo de pesquisa
    st.session_state["pesquisa"] = st.text_input(
        label="Pesquisa de indicadores",
        value="",
        # label_visibility="collapsed",
        help="Pesquisa indicadores por nome, código ou conjunto de palavras",
    )

# coluna para o botão de pesquisa
with col_pesquisa_2:
    # espaço para alinhar o botão com o campo de pesquisa
    st.markdown("<div style='margin-top: 29px;'></div>", unsafe_allow_html=True)
    # botão de pesquisa, que aciona a função on_click
    # st.button("🔎", on_click)
    st.button("🔎")


# colunas de filtros para arrumar a interface
col_filtros_1, col_filtros_2, col_filtros_3 = st.columns([2, 3, 1])
# col_filtros_1, col_filtros_2 = st.columns([1, 2])

# coluna com o radio de filtros
with col_filtros_1:
    # radio de filtros para afunilar a pesquisa
    st.session_state["filtros"] = st.radio(
        "Filtro por contratualização",
        options=radio_optioins,
        index=0,
        horizontal=True,
        on_change=on_click(),
        # help="Filtrar por tipo de indicadores",
    )

with col_filtros_2:
    # espaço para alinhar
    # st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
    # with st.popover("Filtro área clínica"):
    # Numero de Indicadores
    st.session_state["filtro_area_clinica"] = st.multiselect(
        "Filtro por área clínica",
        st.session_state["filtered_df"]["Área clínica"].unique(),
        placeholder="Selecione uma ou mais áreas clínicas",
        on_change=on_click,
        # help="Filtrar por area clínica",
    )

on_click()

# Cálculo do numero de indicadores
with col_filtros_3:
    num_indicatores = len(st.session_state["filtered_df"])
    st.metric("Nº de Iidicadores", num_indicatores)


# tab com 2 opções de visualização dos indicadores encontrados: tabela e cartões
# cartões default
cards, table = st.tabs(["Cartões", "Tabela"])

# se não houver indicadores encontrados, mensagem de aviso
if len(st.session_state["filtered_df"]) == 0:
    # mensagem de aviso
    st.warning("Nenhum indicador encontrado")

else:
    # tab com os cartões
    with cards:
        # loop entre todos os indicadores para criar os cartões para cada
        for index, row in st.session_state["filtered_df"].iterrows():
            # função para criar os cartões predifinida
            cartao_indicador(index, row.to_dict())

    with table:
        # dataframe com os indicadores para visualização

        st.dataframe(
            # dataframe com os indicadores para visualização
            st.session_state["showable_df"],
            # configuração da coluna link_sdm para ter o link para o sdm
            column_config={
                "link_sdm": st.column_config.LinkColumn(
                    label="Link",
                    display_text="SDM",
                )
            },
            use_container_width=True,
            # esconder o index
            hide_index=False,
            # ordem das colunas
            column_order=[
                "id",
                "link_sdm",
                "Nome abreviado",
                "Área clínica",
                # "Intervalo Aceitável",
                # "Intervalo Esperado",
                # "anos_disponiveis",
                "Intervalo Aceitável 2023",
                "Intervalo Esperado 2023",
                # "min_aceitavel_2024",
                # "max_aceitavel_2024",
                # "min_esperado_2024",
                # "max_esperado_2024",
                "Intervalo Aceitável 2024",
                "Intervalo Esperado 2024",
                # "min_aceitavel_2023",
                # "max_aceitavel_2023",
                # "min_esperado_2023",
                # "max_esperado_2023",
            ],
        )

    # st.write(st.session_state["pesquisa"])
    # st.write(st.session_state["filtros"])
    # st.write(st.session_state["filtro_area_clinica"])
    # st.write(st.session_state["df"].head())
    # st.write(st.session_state["filtered_df"].head())
    # st.write(st.session_state["showable_df"].head())

bottom_suport_email()
