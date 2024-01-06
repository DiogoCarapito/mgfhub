import pandas as pd
import os
from unidecode import unidecode
from rapidfuzz import process, fuzz


def func():
    return None


def data_source(source):
    # check if source is in ./data folder
    # if not, download from github

    data_files_list = os.listdir("./data")

    if source in data_files_list:
        return pd.read_csv("./data/" + source, index_col=0)

    else:
        url = "https://github.com/DiogoCarapito/datasets_indicadores/raw/main/datasets/indicadores_sdm.csv"
        return pd.read_csv(url, index_col=0)


def upsave_data_source(source):
    url = "https://github.com/DiogoCarapito/datasets_indicadores/raw/main/datasets/indicadores_sdm.csv"
    df = pd.read_csv(url, index_col=0)
    df.to_csv("./data/" + source)
    print(f"{source} saved successfully!")


def filter_df(df, pesquisa, filtros):
    if filtros == "IDE":
        df = df[df["Tipo"] == "IDE"]
    elif filtros == "IDG":
        df = df[df["Tipo"] == "IDG"]
    else:
        pass

    pesquisa = unidecode(pesquisa.lower())

    if pesquisa == "":
        return df
    else:
        # fuzzy search com score cutoff de 59, comparando com indexing
        search_list = process.extract(
            pesquisa,
            df["Designação"],
            scorer=fuzz.WRatio,
            score_cutoff=59,
            limit=50,
        )
        df = df.filter([id[2] for id in search_list], axis=0)

        return df
