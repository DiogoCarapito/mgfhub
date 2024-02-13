import streamlit as st
import re


def gradient_text(text):
    st.markdown(
        f'<span style="background: linear-gradient(to right, #588EF9, #BE1CF3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold; font-size: 22px;">{text}</span>',
        unsafe_allow_html=True,
    )


def page_config():
    st.set_page_config(
        page_title="mgfhub",
        page_icon="assets/favicon.ico",
        layout="wide",
        initial_sidebar_state="auto",
    )


def sidebar_about():
    # st.sidebar.image("assets/logo.png", use_column_width=True)
    st.sidebar.page_link("https://diogocarapito.com/", label="diogocarapito.com")
    st.sidebar.page_link("https://github.com/DiogoCarapito,", label="Github")
    st.sidebar.page_link("https://twitter.com/DiogoCarapito", label="Twitter")
    st.sidebar.page_link(
        "https://www.linkedin.com/in/diogo-carapito-564a51262/", label="LinkedIn"
    )


def mgfhub_style(text):
    # if "mgfhub.com" or "/mgfhub" apperars in the text, then the text will not be styled
    if "mgfhub.com" in text.lower() or "/mgfhub" in text.lower():
        return text

    # if "mgfhub" apperars in the text, then the text will be styled
    # if "mgfhub" appears in the text, then the text will be styled
    elif "mgfhub" in text.lower():
        # replace all occurrences of "mgfhub" with the styled version
        text = re.sub(
            r"(mgfhub)",
            r'<span style="background: linear-gradient(to right, #588EF9, #BE1CF3); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: bold;">\1</span>',
            text,
            flags=re.I,
        )
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


def main_subheader(text):
    st.markdown(
        "<style>"
        ".gradient-text {"
        "display: inline-block;"  # Changed from inline to inline-block
        "font-size: 2em;"
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


def card_container(title, text, image, link, em_construcao):
    if em_construcao:
        msg_construcao = "🏗️ Em Construção 🏗️"
    else:
        msg_construcao = ""

    with st.container():
        st.markdown(
            f'<a href="{link}" target="_self" style="text-decoration: none; color: inherit;">'
            f'<div style="text-align: center; border: 0px solid #ddd; border-radius: 10px; padding: 10px 20px 10px 20px; background: linear-gradient(135deg, rgba(88, 142, 249, 0.07), rgba(190, 28, 243, 0.07));">'
            f"<h2>{title}</h2>"
            f'<p style="font-size: 19px;">{msg_construcao}</p>'
            f'<p style="font-size: 19px;">{mgfhub_style(text)}</p>'
            "</div>"
            "</a>",
            unsafe_allow_html=True,
        )
        if image:
            st.markdown(
                f'<img src="{image}" style="width: 100%;">',
                unsafe_allow_html=True,
            )


def web_link(label, link, icon):
    st.markdown(
        f'<div style="margin: 5px 0;">'
        f'<a href="{link}" target="_self" style="text-decoration: underline; font-size: 18px;">'
        f'<img src="{icon}" alt="icon" width="20" height="20" style="vertical-align: middle; margin-right: 5px;">'
        f"{label}"
        "</a>"
        "</div>",
        unsafe_allow_html=True,
    )


def cartao_indicador(id, row):
    st.markdown(
        f'<table style="width:100%; border:0; border-collapse: collapse;">'
        f"<tr>"
        f'<td style="width:10%; border:0; vertical-align: top;"><a href="https://sdm.min-saude.pt/BI.aspx?id={id}" style="color: #758AF1; font-size: 24px; font-family: \'IBM Plex Sans\', sans-serif; text-decoration: underline;">{id}</a></td>'
        f'<td style="width:90%; border:0;">'
        f'<div style="display: flex; align-items: center; height: 100%;">'
        f'<div style="font-size: 22px; font-weight: 600; margin: 0 0 4px 0;">{row["Designação"]}</div>'
        f"</div>"
        f'<div style="font-size: 16px; font-weight: 600; margin: 4px 0 0 0;">Área clínica</div>'
        f'<div style="display: flex; align-items: center; height: 100%;">'
        f'<div style="font-size: 14px; font-weight: 450; margin: 0 0 4px 0;">{row["Área clínica"]}</div>'
        f"</div>"
        f'<div style="font-size: 16px; font-weight: 600; margin: 4px 0 0 0;">Descrição</div>'
        f'<div style="display: flex; align-items: center; height: 100%;">'
        f'<div style="font-size: 14px; font-weight: 450; margin: 0 0 4px 0;">{row["Descrição do Indicador"]}</div>'
        f"</div>"
        f'<div style="font-size: 16px; font-weight: 600; margin: 4px 0 0 0;">Intervalo Aceitável: </div>'
        f'<div style="display: flex; align-items: center; height: 100%;">'
        f'<div style="font-size: 14px; font-weight: 450; margin: 0 0 4px 0;"> {row["Intervalo Aceitável"]}</div>'
        f"</div>"
        f'<div style="font-size: 16px; font-weight: 600; margin: 4px 0 4px 0;">Intervalo Esperado: </div>'
        f'<div style="display: flex; align-items: center; height: 100%;">'
        f'<div style="font-size: 14px; font-weight: 450; margin: 0 0 4px 0;"> {row["Intervalo Esperado"]}</div>'
        f"</div>"
        f"</td>"
        f"</tr>"
        f"</table>",
        unsafe_allow_html=True,
    )


def em_desenvolvimento():
    st.write("")
    with st.container(border=True):
        st.markdown(
            '<div style="text-align: center;">'
            "<h1>🏗️ Em construção 🏗️</h1>"
            '<p style="font-size: 19px;">Esta página está em desenvolvimento.</p>'
            "</div>",
            unsafe_allow_html=True,
        )
    st.write("")


def changelog_card(version, date, description):
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 4])

        with col1:
            st.markdown(
                f'<div style="text-align: left;">' f"<h5>{version}</h5>" "</div>",
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                f'<div style="text-align: left;">'
                f'<p style="font-size: 18px;">{date}</p>'
                "</div>",
                unsafe_allow_html=True,
            )

        with col3:
            st.markdown(
                mgfhub_style(description),
                # f'<div style="text-align: left;">'
                # f'<p style="font-size: 16px;">{description}</p>'
                # "</div>",
                unsafe_allow_html=True,
            )
        st.write("")


def centered_title(title):
    st.markdown(
        f'<div style="text-align: center;">' f"<h2>{title}</h2>" "</div>",
        unsafe_allow_html=True,
    )


def centered_text(text):
    text = mgfhub_style(text)
    st.markdown(
        f"{text}",
        # f'<div style="text-align: center;">'
        # f'<p style="font-size: 19px;">{text}</p>'
        # "</div>",
        unsafe_allow_html=True,
    )


def bem_vindos_2(text):
    st.markdown(
        f'<p style="text-align: center; font-size: 22px; font-weight: bold;">{text}</p>',
        unsafe_allow_html=True,
    )


def outros_projetos_card(name, link, description):
    with st.container():
        col1, col2 = st.columns([1, 3])

        with col1:
            st.markdown(
                f'<div style="text-align: left;">'
                f'<a href="{link}"><p style="font-size: 20px;">{name}</p></a>'
                "</div>",
                unsafe_allow_html=True,
            )

        with col2:
            st.markdown(
                mgfhub_style(description),
                # f'<div style="text-align: left;">'
                # f'<p style="font-size: 16px;">{description}</p>'
                # "</div>",
                unsafe_allow_html=True,
            )
        st.write("")
