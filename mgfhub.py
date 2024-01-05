import streamlit as st


def main():
    st.set_page_config(
        page_title="mgfhub 2.0",
        page_icon="assets/favicon.ico",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    

    st.title("mgfhub 2.0")

    st.write("Hello, world!")


if __name__ == "__main__":
    main()
