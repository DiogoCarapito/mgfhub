import streamlit as st

st.title("Sunburst")

radio = st.radio(
    "Modelo Contratual",
    ["IDE", "IDG"],
    horizontal=True
)