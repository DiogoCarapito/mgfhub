import streamlit as st
from utils.style import main_title, em_desenvolvimento

main_title("Sunburst")

radio = st.radio("Modelo Contratual", ["IDE", "IDG"], horizontal=True)

em_desenvolvimento()
