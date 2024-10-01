import streamlit as st


def visualization_options_ui(df_bicsp):
    opções_visualizacao = (
        [
            "Sunburst",
            "Tabela",
            "Sunburst + Tabela",
            "Dumbbell",
            "Sunburst + Sunburst",
        ]
        if len(df_bicsp) > 1
        else ["Sunburst", "Tabela", "Sunburst + Tabela", "Dumbbell"]
    )

    # Dumbbell chart by default if more than one file uploaded
    index_visualizacao = 3 if len(df_bicsp) > 1 else 0

    # radio escolha visualização
    return st.radio(
        "Visualização",
        opções_visualizacao,
        horizontal=True,
        index=index_visualizacao,
        # label_visibility="collapsed",
        key="opcao_visualizacao_ui_1",
    )
