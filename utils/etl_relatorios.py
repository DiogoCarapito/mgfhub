import pandas as pd
import re
import streamlit as st
from mimufs.processing import medico

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# load .env file
load_dotenv()

# Supabase configuration
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# Function to insert data into Supabase
def supabase_record(unidade, ano, mes, tipo):
    # Get current datetime
    date_time = datetime.now().isoformat()

    # Create the data in a format to be inserted into Supabase
    sb_insert = {
        "created_at": date_time,
        "unidade": unidade,
        "ano": ano,
        "mes": mes,
        "tipo": tipo,
    }

    # Insert data into Supabase
    supabase.table("ide_uploads").insert(sb_insert).execute()


def correção_vacina_gripe_435(df):
    df.loc[df["id"] == 435, "Resultado"] = 68.3
    df.loc[df["id"] == 435, "Score"] = 2
    return df


def extrair_id(df, coluna):
    # extrair o id que se econtra entre dois . (pontos) e transformar em int
    # exemplo de input: "2013.001.01 FL" output 1
    return df[coluna].str.extract(r"\.(\d+)\.", expand=False).astype(int)


def etiqueta_ano_completo(df, ano, list_texto):
    list_etiquetas = []

    ano = 2024

    for each in list_texto:
        etiqueta = f"{each} {ano}"
        if etiqueta not in df.columns:
            etiqueta = f"{each} 2024"
        list_etiquetas.append(etiqueta)

    return list_etiquetas


def etiqueta_ano(df, ano):
    # cria as etiquetas para os intervalos aceitáveis e esperados com o ano correcto correspondente aos dados extraídos
    ano = 2024

    int_aceit = f"Intervalo Aceitável {ano}"
    int_esper = f"Intervalo Esperado {ano}"

    # caso não haja intervalos para o ano dos dados, por definição usa os intervalos de 2023
    if int_aceit not in df.columns or int_esper not in df.columns:
        int_aceit = "Intervalo Aceitável 2024"
        int_esper = "Intervalo Esperado 2024"

    return int_aceit, int_esper


def calculate_score_mimuf(row):
    if (
        row["Valor"] > row["Máximo Aceitável 2024"]
        or row["Valor"] < row["Mínimo Aceitável 2024"]
    ):
        return 0
    elif row["Mínimo Aceitável 2024"] <= row["Valor"] < row["Mínimo Esperado 2024"]:
        score_min = (
            2
            * (row["Valor"] - row["Mínimo Aceitável 2024"])
            / (row["Mínimo Esperado 2024"] - row["Mínimo Aceitável 2024"])
        )
        return score_min
    elif row["Máximo Esperado 2024"] < row["Valor"] <= row["Máximo Aceitável 2024"]:
        score_max = (
            2
            * (row["Máximo Aceitável 2024"] - row["Valor"])
            / (row["Máximo Aceitável 2024"] - row["Máximo Esperado 2024"])
        )
        return score_max
    elif row["Mínimo Esperado 2024"] <= row["Valor"] <= row["Máximo Esperado 2024"]:
        return 2
    else:
        return "Error"  # Return some value or raise an exception in case none of the conditions are met


def calculate_score_bicsp(row):
    if (
        row["Resultado"] > row["Máximo Aceitável 2024"]
        or row["Resultado"] < row["Mínimo Aceitável 2024"]
    ):
        return 0
    elif row["Mínimo Aceitável 2024"] <= row["Resultado"] < row["Mínimo Esperado 2024"]:
        score_min = (
            2
            * (row["Resultado"] - row["Mínimo Aceitável 2024"])
            / (row["Mínimo Esperado 2024"] - row["Mínimo Aceitável 2024"])
        )
        return score_min
    elif row["Máximo Esperado 2024"] < row["Resultado"] <= row["Máximo Aceitável 2024"]:
        score_max = (
            2
            * (row["Máximo Aceitável 2024"] - row["Resultado"])
            / (row["Máximo Aceitável 2024"] - row["Máximo Esperado 2024"])
        )
        return score_max
    elif row["Mínimo Esperado 2024"] <= row["Resultado"] <= row["Máximo Esperado 2024"]:
        return 2
    else:
        return "Error"  # Return some value or raise an exception in case none of the conditions are met


def etl_bicsp(list_of_files):
    if list_of_files is None:
        return None

    dict_dfs = {}

    dict_of_dfs = {
        xlsx_file.name: pd.read_excel(xlsx_file, engine="openpyxl")
        for xlsx_file in list_of_files
    }

    for file_name, df in dict_of_dfs.items():
        # get the file name
        unidade = file_name

        # processamento se o ficherio tiver cabeçalho (summarized e underalying data)
        first_column_name = df.columns[0]
        if first_column_name.startswith("Applied"):
            # get the text int he header of the first column
            unidade = re.search(r"Nome UF is (.*)", first_column_name).group(1)

            # remove the first row
            df = df[1:]
            df.columns = df.iloc[0]
            df = df[1:]

            # reset index
            df.reset_index(drop=True, inplace=True)

        # remove any row with "Designação Indicador (+ID)" None
        df = df[df["Designação Indicador (+ID)"].notnull()]

        # extrair o id do "Cód. Indicador"
        df["id"] = extrair_id(df, "Cód. Indicador")

        # make id the index
        # df.set_index("id", inplace=True)

        # sort by id
        df.sort_values("id", inplace=True)

        # Eextração do mês e ano
        ano_mes = str(df["Mês Ind"].unique().max())
        ano = ano_mes[:4]
        mes = ano_mes[4:6]

        # nome = f"{unidade} {ano}/{mes}"
        nome = f"{unidade} {mes}/{ano}"

        # correção_vacina_gripe_435(df)

        df["Resultado"] = df["Resultado"].astype(float)

        sf_portaria = pd.read_csv("./data/sunburst_portaria_411a_2023.csv")

        colunas_portaria = [
            "id",
            "Nome",
            "Dimensão",
            "Ponderação",
            "Lable",
        ]

        etiquetas_intervalos_ano = etiqueta_ano_completo(
            df,
            ano,
            [
                "Intervalo Aceitável",
                "Mínimo Aceitável",
                "Máximo Aceitável",
                "Intervalo Esperado",
                "Mínimo Esperado",
                "Máximo Esperado",
            ],
        )

        colunas_portaria.extend(etiquetas_intervalos_ano)

        df = df.merge(
            sf_portaria[colunas_portaria],
            on="id",
            how="right",
        )

        df["Score"] = df.apply(calculate_score_bicsp, axis=1)

        # drop the rows with Score "Error"
        df = df[df["Score"] != "Error"]

        df["Score"] = df["Score"].astype(float)

        # Update list_of_dfs with the new df
        dict_dfs[nome] = {
            "data": df[["id", "Resultado", "Score", "Mês Ind"]],
            "nome": nome,
            "ano": int(ano),
            "mes": int(mes),
            "unidade": unidade,
        }

        supabase_record(unidade, ano, mes, "bicsp")

    return dict_dfs


def merge_portaria_bicsp(df_bicsp, ano):
    df_portaria = pd.read_csv("./data/sunburst_portaria_411a_2023.csv")

    # df_portaria.loc[df_portaria["Nome"]=="IDE", "Ponderação"] = 100

    df = df_portaria.merge(
        df_bicsp[["id", "Resultado", "Score", "Mês Ind"]],
        on="id",
        how="left",
    )

    # list of dimensions and drop empty obnes
    list_dimensoes = [x for x in df["Dimensão"].unique().tolist() if pd.notna(x)]

    # remove IDE
    list_dimensoes = list_dimensoes[1:]

    # calculate the score for each dimension based on the average wheighed score
    df["contributo"] = df["Ponderação"] * df["Score"] / 2

    for dim in list_dimensoes:
        df.loc[df["Nome"] == dim, "Resultado"] = df[df["Dimensão"] == dim][
            "contributo"
        ].sum()

    df.loc[df["Dimensão"] == "IDE", "Score"] = (
        2
        * df.loc[df["Dimensão"] == "IDE", "Resultado"]
        / df.loc[df["Dimensão"] == "IDE", "Ponderação"]
    )

    # apagar intervalos que não fazem sentido
    int_aceit, int_esper = etiqueta_ano(df, ano)
    df.loc[df["Dimensão"] == "IDE", int_aceit] = "N/A"
    df.loc[df["Dimensão"] == "IDE", int_esper] = "N/A"
    df.loc[df["Nome"] == "IDE", int_aceit] = "N/A"
    df.loc[df["Nome"] == "IDE", int_esper] = "N/A"

    # IDE
    df.loc[df["Nome"] == "IDE", "Resultado"] = df.loc[
        df["Dimensão"] == "IDE", "Resultado"
    ].sum()
    df.loc[df["Nome"] == "IDE", "Score"] = (
        2
        * df.loc[df["Nome"] == "IDE", "Resultado"]
        / df.loc[df["Nome"] == "IDE", "Ponderação"]
    )

    df.loc[df["Nome"] != "IDE"] = df.loc[df["Nome"] != "IDE"].fillna(0)

    # make score a float
    df["Score"] = df["Score"].astype(float)

    # st.write(
    #     df[["id", "Nome", "Dimensão", "Ponderação", "Resultado", "Score", "contributo"]]
    # )

    # st.write(df[["Lable", "Score"]].dtypes)

    return df


def etl_mimuf(list_of_files):
    if list_of_files is None:
        return None

    dict_dfs = {}

    dict_of_dfs = {
        xlsx_file.name: pd.read_excel(xlsx_file, engine="openpyxl")
        for xlsx_file in list_of_files
    }

    # for loop to process each file
    for df in dict_of_dfs.values():
        # main ETL
        # if the first row begins with P02_01_R03

        if df.columns.shape[0] != 10:
            st.warning("O ficheiro não está correcto")

        ano_mes = df.columns[7]
        ano = ano_mes[:4]
        mes = ano_mes[5:7]

        # remove the first row
        df = df[1:]
        df.reset_index(drop=True, inplace=True)

        # #give name to columns
        df.columns = [
            "Unidade",
            "para_remover_1",
            "id",
            "para_remover_2",
            "Médico Familia",
            "para_remover_3",
            "para_remover_4",
            "Numerador",
            "Denominador",
            "Valor",
        ]

        # list_medicos = df["Médico Familia"].unique()
        # # replace the names of "Médico Familia" to a generic name "Médico 1"
        # for index, each in enumerate(list_medicos):
        #     df.loc[df["Médico Familia"] == each, "Médico Familia"] = f"Médico {index+1}"

        unidade = df["Unidade"].unique()[0]
        nome = f"{unidade} {mes}/{ano}"

        # drop column "Mês"
        df.drop(
            columns=[
                "Unidade",
                "para_remover_1",
                "para_remover_2",
                "para_remover_3",
                "para_remover_4",
            ],
            inplace=True,
        )

        # Uniformizar nomes de médicos
        df = medico(df, column="Médico Familia")

        # extrair id indicador
        df["id"] = extrair_id(df, "id")

        # make id the index
        df.set_index("id", inplace=True)

        etiquetas_intervalos_ano = etiqueta_ano_completo(
            df,
            ano,
            [
                "Intervalo Aceitável",
                "Mínimo Aceitável",
                "Máximo Aceitável",
                "Intervalo Esperado",
                "Mínimo Esperado",
                "Máximo Esperado",
            ],
        )

        # get sunburst_portaria csv
        df_portaria = pd.read_csv("./data/sunburst_portaria_411a_2023.csv")

        colunas_portaria = [
            "id",
            "Nome",
            "Dimensão",
            "Ponderação",
            "Lable",
        ]

        colunas_portaria.extend(etiquetas_intervalos_ano)

        # merge df with df_portaria
        df = df.merge(
            df_portaria[colunas_portaria],
            on="id",
            how="left",
        )
        # drop rows with NaN
        # df.dropna(subset=["id"], inplace=True)

        df.reset_index(drop=True, inplace=True)

        df["Valor"] = df["Valor"].str.replace(",", ".").astype(float)

        # sort by id
        df.sort_values("id", inplace=True)

        # score calculado a partir do valor do indicador e dos intervalos aceitável e esperado
        # se acima do máximo aceitave ou abaixo do mínimo aceitavel, score = 0
        # se entre o minimo e maxio esperado, score = 2
        # se entre minimo aceitabel e minimo esperado ou entre maximo esperado e maximo aceitavel, score = 1
        # se acima do maximo esperado mas abaico do maximo aceitavel, score = 1
        # valores aceitáveis e esperados estão noutra coluna e deve ser usados o da mesma linha

        df["Score"] = df.apply(calculate_score_mimuf, axis=1)

        # Numerador need to substitute , to . and transform to float
        df["Numerador"] = (
            df["Numerador"].str.replace(".", "").str.replace(",", ".").astype(float)
        )

        # calculate the score for each dimension based on the average wheighed score
        df["contributo"] = df["Ponderação"] * df["Score"] / 2

        # list of dimensions and drop empty obnes
        list_dimensoes = [x for x in df["Dimensão"].unique().tolist() if pd.notna(x)]

        # remove IDE
        list_dimensoes = list_dimensoes[1:]

        for dim in list_dimensoes:
            df.loc[df["Nome"] == dim, "Resultado"] = df[df["Dimensão"] == dim][
                "contributo"
            ].sum()

        df.loc[df["Dimensão"] == "IDE", "Score"] = (
            2
            * df.loc[df["Dimensão"] == "IDE", "Resultado"]
            / df.loc[df["Dimensão"] == "IDE", "Ponderação"]
        )

        # apagar intervalos que não fazem sentido
        int_aceit, int_esper = etiqueta_ano(df, ano)
        df.loc[df["Dimensão"] == "IDE", int_aceit] = "N/A"
        df.loc[df["Dimensão"] == "IDE", int_esper] = "N/A"
        df.loc[df["Nome"] == "IDE", int_aceit] = "N/A"
        df.loc[df["Nome"] == "IDE", int_esper] = "N/A"

        # IDE
        df.loc[df["Nome"] == "IDE", "Resultado"] = df.loc[
            df["Dimensão"] == "IDE", "Resultado"
        ].sum()
        df.loc[df["Nome"] == "IDE", "Score"] = (
            2
            * df.loc[df["Nome"] == "IDE", "Resultado"]
            / df.loc[df["Nome"] == "IDE", "Ponderação"]
        )

        df.loc[df["Nome"] != "IDE"] = df.loc[df["Nome"] != "IDE"].fillna(0)

        # rename columns to remove year
        # df.rename(columns=lambda x: re.sub(r" 2023", "", x), inplace=True)

        # st.write(df["Médico Familia"].unique())
        # st.write(df["Médico Familia"].unique().shape[0])
        # st.write(df["id"].unique())
        # st.write(df["id"].unique().shape[0])

        # save as a dictionary name:df
        dict_dfs[nome] = {
            "df": df,
            "ano": ano,
            "mes": mes,
            "unidade": unidade,
            "nome": nome,
        }

        supabase_record(unidade, ano, mes, "mimuf")

    return dict_dfs
