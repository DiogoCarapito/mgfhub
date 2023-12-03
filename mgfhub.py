import streamlit as st


def main():
    st.set_page_config(
        page_title="mgfhub 2.0",
        page_icon="assets/favicon.ico",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    with st.sidebar:
        st.title("📄 Upload")
        st.write("Upload your file here:")
        uploaded_file = st.file_uploader("Choose a file", type="csv")
        if uploaded_file is not None:
            st.write("File uploaded successfully!")
            st.write(uploaded_file)
        else:
            st.write("Please upload a file!")

    st.title("mgfhub 2.0")

    st.write("Hello, world!")


if __name__ == "__main__":
    main()
