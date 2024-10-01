import streamlit as st
from utils.etl_relatorios import (
    etl_bicsp,
    etl_mimuf,
    extracao_areas_clinicas,
    merge_portaria_bicsp,
    process_indicador,
)
from utils.vis_relatorios import (
    sunburst_bicsp,
    dumbbell_plot,
    tabela,
    ide_bar,
    horizontal_bar,
    sunburst_mimuf,
)
