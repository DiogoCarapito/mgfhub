import streamlit as st
from utils.style import main_title, em_desenvolvimento, sidebar_about

main_title("Sunburst")

sidebar_about()

radio = st.radio("Modelo Contratual", ["IDE", "IDG"], horizontal=True)

em_desenvolvimento()
