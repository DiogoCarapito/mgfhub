import streamlit as st
from utils.style import main_title, em_desenvolvimento, sidebar_about

main_title("Perguntas Frequentes")

sidebar_about()

st.subheader("1. qual a diferença entre IDE e IDG?")
st.write("Explicação...")

st.subheader("2. qual a difernça entre indicador Fixo e Flutuante?")
st.write("Explicação...")

st.subheader("3. como é que se calcula o IDE?")
st.write("Explicação...")

st.subheader("4. quando é que é melhor usar um indicador Fixo?")
st.write("Explicação...")

st.subheader("5. quando é que é melhor usar um indicador Flutuante?")
st.write("Explicação...")

st.divider()

em_desenvolvimento()
