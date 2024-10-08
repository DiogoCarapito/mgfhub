import pandas as pd
import os
from scripts.load_data import download_update_data
import streamlit as st


@st.cache_data
def data_source(source):
    # check if source is in ./data folder
    # if not, download from github

    data_files_list = os.listdir("./data")

    if source in data_files_list:
        return pd.read_csv("./data/" + source, index_col=0)

    else:
        download_update_data(source)
        return pd.read_csv("./data/" + source, index_col=0)
