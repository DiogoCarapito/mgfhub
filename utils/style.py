import streamlit as st


def main_title(text):
    st.markdown(
        "<style>"
        ".gradient-text {"
        "display: inline-block;"  # Changed from inline to inline-block
        "font-size: 4em;"
        "font-weight: bold;"
        "width: 100%;"  # Added to make the span span the entire width
        "text-align: center;}"  # Added to center the text
        ".gradient {"
        "background: linear-gradient(to right, #588EF9, #BE1CF3);"
        "-webkit-background-clip: text;"
        "-webkit-text-fill-color: transparent;}"
        "</style>"
        f'<span class="gradient-text"><span class="gradient">{text}</span></span>',
        unsafe_allow_html=True,
    )


def web_link(label, link, icon):
    st.markdown(
        f'<a href="{link}" target="_self" style="text-decoration: none; color: #7568F3; font-size: 16px;">'
        f'<img src="{icon}" alt="icon" width="16" height="16" style="vertical-align: middle; margin-right: 5px;">'
        f"{label}"
        "</a>",
        unsafe_allow_html=True,
    )
