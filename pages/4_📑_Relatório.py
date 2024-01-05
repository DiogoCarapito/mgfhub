import streamlit as st

st.title("Relatório")

with st.sidebar:
        st.title("📄 Upload")
        st.write("Upload your file here:")
        uploaded_file = st.file_uploader("Choose a file", type="csv")
        if uploaded_file is not None:
            st.write("File uploaded successfully!")
            st.write(uploaded_file)
        else:
            st.write("Please upload a file!")