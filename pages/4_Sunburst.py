import streamlit as st
from utils.style import page_config, main_title, em_desenvolvimento

page_config()

main_title("Sunburst")

em_desenvolvimento()

# sidebar_about()

radio = st.radio("Modelo Contratual", ["IDE", "IDG"], horizontal=True)
