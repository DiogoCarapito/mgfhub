import streamlit as st
from utils.style import page_config, main_title, bottom_suport_email, em_desenvolvimento
from utils.ide_ui import (
    ide_sidebar,
    tab_visao_unidade,
    tab_visao_equipas,
    tab_visao_profissional,
)

import pandas as pd

from utils.vis_relatorios import sunburst_bicsp

page_config()

main_title("IDE")

# variaveis iniciais
# Dicinoários para guardar os dataframes carregados
st.session_state["df_bicsp"] = {}
st.session_state["df_mimuf"] = {}

# opções de visualização
st.session_state["opcao_visualizacao"] = "Sunburst"
st.session_state["opcao_visualizacao_2"] = "Barras + Tabela"

# mensagens de alerta de ficheiros não carregados
bicsp_nao_carregado = "Ficheiros do BI-CSP não carregados!"
mimuf_nao_carregado = "Ficheiros do MIM@UF não carregados!"

# Sidebar with uplods of xlsx files after etl
st.session_state["df_bicsp"], st.session_state["df_mimuf"] = ide_sidebar()


@st.cache_data
def load_data_sunburst():
    # load a dummy sunburst with score 1 in all parameters
    bicsp_score_1 = pd.read_csv("data/sunburst_score_1.csv", sep=";")

    return bicsp_score_1


# Tabs
tab_unidade, tab_equipas, tab_prof_geral, tab_nao_ide = st.tabs(
    [
        "Visão de Unidade",
        "Visão de Equipas",
        "Visão por Profissional",
        "Indicadores não-IDE",
    ],
)

with tab_unidade:
    # mensagem se não houver ficheiros carregados
    if not st.session_state["df_bicsp"]:
        # warning message
        st.warning(bicsp_nao_carregado)

        st.divider()
        sunburst_bicsp(load_data_sunburst(), 2000, "Janeiro", "USF ?", 800)

    else:
        tab_visao_unidade()


with tab_equipas:
    if not st.session_state["df_mimuf"]:
        st.warning(mimuf_nao_carregado)

    else:
        tab_visao_equipas()


with tab_prof_geral:
    # centered_title("Profissional - Visão Geral")

    if not st.session_state["df_mimuf"]:
        st.warning(mimuf_nao_carregado)

    elif len(st.session_state["df_mimuf"]) >= 1:
        tab_visao_profissional()


with tab_nao_ide:
    em_desenvolvimento()

    st.write("")
    st.write(
        "Futura visualização de indicadores que não contam para o IDE mas podem ser relevantes monitorizar para auditorias internas ou para preparar mudanças no IDE"
    )
    st.write("")


bottom_suport_email()
