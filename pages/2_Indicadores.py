import streamlit as st
from utils.utils import data_source, filter_df
from utils.style import main_title, cartao_indicador, sidebar_about

# carregar o dataframe com os indicadores
st.session_state["df"] = data_source("indicadores_sdm_complete.csv")

# campode pesquisa inicial
st.session_state["pesquisa"] = ""

# opções de filtros para o radio
radio_optioins = ["IDE", "IDG", "Todos"]

# index inicial do radio
radio_starting_index = 0

# opção de filtro inicial
st.session_state["filtros"] = radio_optioins[radio_starting_index]


# função para executar a pesquisa, é chamada quando o botão de pesquisa é clicado ou quando a página é aberta
# (mesmo quando o Enter é clicado no st.text_input)
def on_click():
    # função para filtrar o dataframe com base na pesquisa e nos filtros
    st.session_state["filtered_df"] = filter_df(
        st.session_state["df"],
        st.session_state["pesquisa"],
        st.session_state["filtros"],
    )

    # dataframe com os indicadores para visualização, filtrando as colunas que não são necessárias
    st.session_state["showable_df"] = st.session_state["filtered_df"].drop(
        columns=["search_indexes", "ide", "idg", "Área | Subárea | Dimensão"]
    )

    # tab com 2 opções de visualização dos indicadores encontrados: tabela e cartões
    table, cards = st.tabs(["Tabela", "Cartões"])

    # se não houver indicadores encontrados, mensagem de aviso
    if len(st.session_state["filtered_df"]) == 0:
        # mensagem de aviso
        st.warning("Nenhum indicador encontrado")

    else:
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
                use_container_width=False,
                # esconder o index
                hide_index=True,
                # ordem das colunas
                column_order=[
                    "id",
                    "link_sdm",
                    "Nome abreviado",
                    "Área clínica",
                    "Intervalo Aceitável",
                    "Intervalo Esperado",
                ],
            )

        # tab com os cartões
        with cards:
            # loop entre todos os indicadores para criar os cartões para cada
            for index, row in st.session_state["filtered_df"].iterrows():
                # função para criar os cartões predifinida
                cartao_indicador(index, row.to_dict())


# titulo principal estilizado com a função main_title
main_title("Indicadores")

# sidebar com os links sociais predefinido
sidebar_about()

# user interface
col_pesquisa_1, col_pesquisa_2 = st.columns([5, 1])

with col_pesquisa_1:
    # campo de pesquisa
    st.session_state["pesquisa"] = st.text_input(
        label="Pesquisa",
        value="",
        label_visibility="collapsed",
        help="Pesquisa por nome, código ou conjunto de palavras",
    )

# coluna para o botão de pesquisa
with col_pesquisa_2:
    # botão de pesquisa, que aciona a função on_click
    st.button("Pesquisar", on_click)


# colunas de filtros para arrumar a interface
col_filtros_1, col_filtros_2 = st.columns(2)

# coluna com o radio de filtros
with col_filtros_1:
    # radio de filtros para afunilar a pesquisa
    st.session_state["filtros"] = st.radio(
        "Filtros",
        index=radio_starting_index,
        horizontal=True,
        # help="Filtrar por tipo de indicadores",
    )

# Execução da pesquisa na abertura da página
on_click()

# Cálculo do numero de indicadores
num_indicatores = len(st.session_state["filtered_df"])

# Coluna com o numero de indicadores encontrados
with col_filtros_2:
    # Numero de indicadores
    st.metric("Número de Indicadores", num_indicatores)