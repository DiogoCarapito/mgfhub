import streamlit as st
from utils.style import page_config, main_title, em_desenvolvimento, bottom_suport_email
from ui.tutorial import tutorial_bicsp, tutorial_mimuf

page_config()

main_title("Perguntas Frequentes")


# tabs sobre o mgfhub e sobre os indicadores
tab_mgfhub, tab_indicadores = st.tabs(["Sobre o mgfhub", "Sobre os Indicadores"])

with tab_mgfhub:
    selection = st.radio(
        "Escolha o tutorial",
        ["BI-CSP", "MIM@UF"],
        horizontal=True,
    )

    if selection == "BI-CSP":
        tutorial_bicsp()
    elif selection == "MIM@UF":
        tutorial_mimuf()

with tab_indicadores:
    em_desenvolvimento()

    # sidebar_about()

    st.subheader("1. Qual a diferença entre IDE e IDG?")
    st.write("Explicação...")

    st.subheader("2. Qual a diferença entre indicador Fixo e Flutuante?")
    st.write("Explicação...")

    st.subheader("3. Como é que se calcula o IDE?")
    st.write("Explicação...")

    st.subheader("4. Quando é que é melhor usar um indicador Fixo?")
    st.write("Explicação...")

    st.subheader("5. Quando é que é melhor usar um indicador Flutuante?")
    st.write("Explicação...")

bottom_suport_email()
