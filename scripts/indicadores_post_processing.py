import pandas as pd
import numpy as np
from unidecode import unidecode

df = pd.read_csv("../data/scrapped_indicadores.csv")

# Load dos intervalos aceitávels e esperados
df_intervalos = pd.read_csv("../data/scrapped_intervalos.csv")
df = df.merge(df_intervalos, on="id", how="outer")
df.fillna(np.nan, inplace=True)


s = " "
# Criação de uma coluna para indexação, que serve de fonte de pesquisa
df["indexing"] = [
    str(row.id)
    + s  # id
    + row.nome_abreviado
    + s  # nome abreviado
    + row.designacao
    + s
    + str(row.area)
    + s  # designacao
    + str(row.subarea)
    + s  # subarea
    + str(row.dimensao)
    + s  # dimensao
    + row.tipo_de_indicador
    + s  # tipo de indicador
    + row.area_clinica  # area clinica
    for index, row in df.iterrows()
]

# Remove accents
df["indexing"] = df["indexing"].str.lower()
df["indexing"] = df["indexing"].apply(unidecode)

# Markdown para ter um link na tabela
df["id_sdm"] = [
    "[" + str(row["id"]) + "](" + row["link"] + ")" for index, row in df.iterrows()
]

# Expoação para csv
df.to_csv("../data/indicadores_post_processed.csv", index=False, header=True)
