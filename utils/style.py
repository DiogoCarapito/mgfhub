import streamlit as st
import re

def mgfhub_style(text):
    # if "mgfhub" apperars in the text, then the text will be styled
    # if "mgfhub" appears in the text, then the text will be styled
    if "mgfhub" in text.lower():
        # replace all occurrences of "mgfhub" with the styled version
        text = re.sub(r"(mgfhub)", r'<span style="background: linear-gradient(to right, #588EF9, #BE1CF3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold;">\1</span>', text, flags=re.I)
        return text
    else:
        return text


def double_space():
    st.markdown("")
    st.markdown("")
    st.markdown("")


def button_link(label):
    st.markdown(
        f'<div style="text-align: center;">'
        f'<a href={label} target="_self">'
        f'<button style="color: white; background: linear-gradient(to right, #588EF9, #BE1CF3); border: none; cursor: pointer; '
        f"padding: 6px 12px; text-align: center; text-decoration: none; display: inline-block; "
        f"border-radius: 8px; -webkit-border-radius: 8px; -moz-border-radius: 8px; "
        f'font-size: 16px; margin: 4px 2px; -webkit-transition-duration: 0.4s; transition-duration: 0.4s;">'
        f"Ir para {label}"
        f"</button></a>"
        f"</div>",
        unsafe_allow_html=True,
    )


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


def intro(text):
    text = mgfhub_style(text)
    st.markdown(
        f'<p style="text-align: center; font-size: 22px;">{text}</p>',
        unsafe_allow_html=True,
    )


def card_container(title, text, image, link):
    with st.container():
        st.markdown(
            f'<div style="text-align: center;">'
            f"<h1>{title}</h1>"
            f'<p style="font-size: 19px;">{text}</p>'
            "</div>",
            unsafe_allow_html=True,
        )
        if image:
            st.image(image, use_column_width=True)
        button_link(link)


def web_link(label, link, icon):
    st.markdown(
        f'<a href="{link}" target="_self" style="text-decoration: none; color: #7568F3; font-size: 16px;">'
        f'<img src="{icon}" alt="icon" width="16" height="16" style="vertical-align: middle; margin-right: 5px;">'
        f"{label}"
        "</a>",
        unsafe_allow_html=True,
    )
