import pandas as pd
import os


def data_source(source):
    # check if source is in ./data folder
    # if not, download from github

    data_files_list = os.listdir("./data")

    if source in data_files_list:
        return pd.read_csv("./data/" + source, index_col=0)

    else:
        url = "https://github.com/DiogoCarapito/datasets_indicadores/raw/main/datasets/indicadores_sdm.csv"
        return pd.read_csv(url, index_col=0)
