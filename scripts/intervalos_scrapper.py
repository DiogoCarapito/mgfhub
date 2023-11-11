import pandas as pd
import tabula
import re

# seleção do documento e paginas com as tabelas
# 2022
# documento = 'data/ACSS-Operacionalizacao_CSP_2022_Final.pdf'
# pages = [76,77,78,79,80]

documento = "data/Operacionalizacao_CSP_2023_VF.pdf"
pages = [74, 75, 76, 77, 78]
# Seleção das paginas onde estão as tabelas


tables = tabula.read_pdf(documento, pages=pages)

df = pd.concat(
    [tables[pages.index(page)].dropna() for page in pages], ignore_index=True
)

"""
for col in df.columns:
    print(col)
"""
# print(df.columns[2])
# regex = '\d+\.*\d'

#
df = df.assign(id=[int(row["ID Indicador"]) for index, row in df.iterrows()])
df = df.drop(columns=["ID Indicador"])
df.rename(
    columns={
        "Nome Indicador": "nome_indicador",
        "Int var.": "intervalo_aceitavel",
        "Int. Esperado": "intervalo_esperado",
    },
    inplace=True,
)

# Regular expressions para extrir os intervalos minimo e máximo
regex_min = "\[(\d*\.*\d)"
regex_max = "(\d*\.*\d)\]"

# Criação de novas colunas com os valores extraidos de min e max dos intervalos aceitáveis e esperados
df = df.assign(
    min_aceitavel=[
        re.findall(regex_min, row["intervalo_aceitavel"])[0]
        for index, row in df.iterrows()
    ]
)
df = df.assign(
    min_esperado=[
        re.findall(regex_min, row["intervalo_esperado"])[0]
        for index, row in df.iterrows()
    ]
)
df = df.assign(
    max_esperado=[
        re.findall(regex_max, row["intervalo_esperado"])[0]
        for index, row in df.iterrows()
    ]
)
df = df.assign(
    max_aceitavel=[
        re.findall(regex_max, row["intervalo_aceitavel"])[0]
        for index, row in df.iterrows()
    ]
)

df = df[
    [
        "id",
        "nome_indicador",
        "min_aceitavel",
        "min_esperado",
        "max_esperado",
        "max_aceitavel",
        "intervalo_aceitavel",
        "intervalo_esperado",
    ]
]

"""for index, row in df.iterrows():
    print(re.findall(regex_max, row['Int. Esperado'])[0])"""

# print(df.head())
"""
for col in df.columns:
    print(col)
"""

df.to_csv("../data/scrapped_intervalos.csv", index=False)
