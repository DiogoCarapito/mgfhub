import streamlit as st


def button_link(label):
    st.markdown(
        f'<a href={label} target="_self">'
        f'<button style="color: white; background-color: #0000F5; border: none; cursor: pointer; '
        f"padding: 6px 12px; text-align: center; text-decoration: none; display: inline-block; "
        f"border-radius: 8px; -webkit-border-radius: 8px; -moz-border-radius: 8px; "
        f'font-size: 16px; margin: 4px 2px; -webkit-transition-duration: 0.4s; transition-duration: 0.4s;">'
        f"Ir para {label}"
        f"</button></a>",
        unsafe_allow_html=True,
    )
