import streamlit as st

# from utils.etl_relatorios import (
#     etl_bicsp,
#     etl_mimuf,
#     extracao_areas_clinicas,
#     merge_portaria_bicsp,
#     process_indicador,
# )

from utils.vis_relatorios import (
    # sunburst_bicsp,
    # dumbbell_plot,
    # tabela,
    # ide_bar,
    # horizontal_bar,
    sunburst_mimuf,
)


# @st.cache_data
def tab_visao_profissional(df_mimuf):
    col_filtro_medico_1, col_filtro_medico_2 = st.columns(2)

    with col_filtro_medico_1:
        dataframe_selected = st.selectbox(
            "Escolha o dataframe",
            df_mimuf,
        )

    with col_filtro_medico_2:
        filtro_medico = st.selectbox(
            "Médico Familia",
            (df_mimuf[dataframe_selected]["df"]["Médico Familia"].unique()),
        )

    sunburst_mimuf(
        df_mimuf[dataframe_selected]["df"][
            df_mimuf[dataframe_selected]["df"]["Médico Familia"] == filtro_medico
        ],
        df_mimuf[dataframe_selected]["ano"],
        df_mimuf[dataframe_selected]["mes"],
        df_mimuf[dataframe_selected]["unidade"],
        800,
    )
