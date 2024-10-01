import streamlit as st
from utils.style import bottom_suport_email


def warning_if_empty(df_bicsp, df_mimuf):
    if not df_bicsp:
        st.warning("Ficheiros do BI-CSP não carregados!")
    if not df_mimuf:
        st.warning("Ficheiros do MIM@UF não carregados!")
        if not df_bicsp:
            bottom_suport_email()
            st.stop()
