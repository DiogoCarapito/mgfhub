import streamlit as st


@st.dialog("Politica de privacidade e de colheita de dados")
def consent_popup():
    # read the terms of use from content/politica_privacidade.md
    with open("content/content_popup.md", "r") as file:
        content_popup = file.read()

    st.markdown(content_popup)

    st.write("")

    # Add links to the terms of use and privacy policy
    col_popup_1, col_popup_2 = st.columns([1, 1])
    with col_popup_1:
        st.page_link(
            "pages/6_Termos_de_utilização.py", label="Termos de utilização", icon="📒"
        )
    with col_popup_2:
        st.page_link(
            "pages/7_Politica_de_privacidade.py",
            label="Politica de privacidade",
            icon="🗒️",
        )

    st.write("")

    # buttons to accept or reject the terms of use and privacy policy
    col_popup_1, col_popup_2 = st.columns([1, 1])

    with col_popup_1:
        if st.button("Aceitar", type="primary"):
            st.session_state["consent"] = True
            st.rerun()

    with col_popup_2:
        if st.button("Não aceitar", type="secondary"):
            st.session_state["consent"] = False
            st.rerun()
