import streamlit as st
from utils.style import main_title

main_title("Sunburst")

radio = st.radio("Modelo Contratual", ["IDE", "IDG"], horizontal=True)
