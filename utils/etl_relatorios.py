import pandas as pd
import re
import streamlit as st

# from mimufs.processing import medico

import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime

# load .env file
load_dotenv()

# key to know the local of the code being run
production = os.environ.get("PRODUCTION")

# Supabase configuration
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)


# Function to insert data into Supabase
@st.cache_data()
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
        # "production": bool(environment),
    }

    # Insert data into Supabase
    supabase.table("ide_uploads").insert(sb_insert).execute()


# From mimufs
@st.cache_data()
def medico(df: pd.DataFrame, column="Médico Familia") -> pd.DataFrame:
    # convert the string to title case
    df.loc[:, column] = df.loc[:, column].str.title()

    # remove the double spaces in the string
    df.loc[:, column] = df.loc[:, column].str.replace("  ", " ")

    # remove the last space in the string
    df.loc[:, column] = df.loc[:, column].str.rstrip()

    return df


@st.cache_data()
def extrair_id(df, coluna):
    # remove columns with BA

    # drop rows that end in "FX", but keep "2020.435.01 FX"
    df = df[~(df[coluna].str.endswith("FX") & (df[coluna] != "2020.435.01 FX"))]

    # extrair o id que se econtra entre dois . (pontos) e transformar em int
    # exemplo de input: "2013.001.01 FL" output 1

    df[coluna] = (
        df[coluna].str.extract(r"\.(\d+)\.", expand=False).fillna(0).astype(int)
    )

    return df


@st.cache_data()
def etiqueta_ano_completo(df, ano, list_texto):
    list_etiquetas = []

    ano = 2024

    for each in list_texto:
        etiqueta = f"{each} {ano}"
        if etiqueta not in df.columns:
            etiqueta = f"{each} 2024"
        list_etiquetas.append(etiqueta)

    return list_etiquetas


@st.cache_data()
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


@st.cache_data()
def calculate_score_mimuf(row):
    # Convert the values to floats
    valor = float(row["Valor"])
    min_aceitavel = float(row["Mínimo Aceitável 2024"])
    min_esperado = float(row["Mínimo Esperado 2024"])
    max_esperado = float(row["Máximo Esperado 2024"])
    max_aceitavel = float(row["Máximo Aceitável 2024"])

    if valor > max_aceitavel or valor < min_aceitavel:
        return 0
    elif min_aceitavel <= valor < min_esperado:
        score_min = 2 * (valor - min_aceitavel) / (min_esperado - min_aceitavel)
        return score_min
    elif max_esperado < valor <= max_aceitavel:
        score_max = 2 * (max_aceitavel - valor) / (max_aceitavel - max_esperado)
        return score_max
    elif min_esperado <= valor <= max_esperado:
        return 2
    else:
        return 0  # Return some value or raise an exception in case none of the conditions are met


@st.cache_data()
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


@st.cache_data()
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
        # versão ENG
        if first_column_name.startswith("Applied"):
            # get the text int he header of the first column
            unidade = re.search(r"Nome UF is (.*)", first_column_name).group(1)

            # remove the first row
            df = df[1:]
            df.columns = df.iloc[0]
            df = df[1:]

            # reset index
            df = df.reset_index(drop=True)

        # versão PT
        elif first_column_name.startswith("Filtros"):
            unidade = re.search(r"Nome UF é (.*)", first_column_name).group(1)

            # remove the first row
            df = df[1:]
            df.columns = df.iloc[0]
            df = df[1:]

            # reset index
            df = df.reset_index(drop=True)

        # remove any row with "Designação Indicador (+ID)" None
        df = df[df["Designação Indicador (+ID)"].notnull()]

        # extrair o id do "Cód. Indicador"
        df = extrair_id(df, "Cód. Indicador")

        # rename "Cód. Indicador" to "id"
        df = df.rename(columns={"Cód. Indicador": "id"})

        # make id the index
        # df.set_index("id", inplace=True)

        # sort by id
        df = df.sort_values("id")

        # check if df["Hierarquia Contratual - Área"] has "IDE - Desempenho" and keep only those rows
        if df["Hierarquia Contratual - Área"].str.contains("IDE - Desempenho").any():
            df = df[df["Hierarquia Contratual - Área"].str.contains("IDE - Desempenho")]

        # Eextração do mês e ano
        ano_mes = str(df["Mês Ind"].unique().max())
        # ano = "2024"
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
            "Área clínica",
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
            "data": df[
                [
                    "id",
                    "Resultado",
                    "Score",
                    "Ponderação",
                    "Mês Ind",
                    "Hierarquia Contratual - Área",
                    "Área clínica",
                ]
            ],
            "nome": nome,
            "ano": int(ano),
            "mes": int(mes),
            "unidade": unidade,
        }

        supabase_record(unidade, ano, mes, "bicsp")

    return dict_dfs


@st.cache_data()
def merge_portaria_bicsp(df_bicsp, ano):
    df_portaria = pd.read_csv("./data/sunburst_portaria_411a_2023.csv")

    # df_portaria.loc[df_portaria["Nome"]=="IDE", "Ponderação"] = 100

    df = df_portaria.merge(
        df_bicsp[
            [
                "id",
                "Resultado",
                "Score",
                "Mês Ind",
                "Hierarquia Contratual - Área",
                "Área clínica",
            ]
        ],
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

    # df.loc[df["Nome"] != "IDE"] = df.loc[df["Nome"] != "IDE"].fillna(0)

    # make score a float
    df["Score"] = df["Score"].astype(float)

    # remove id column
    # df.drop(columns=["id"], inplace=True)

    # st.write(
    #     df[["id", "Nome", "Dimensão", "Ponderação", "Resultado", "Score", "contributo"]]
    # )

    # st.write(df[["Lable", "Score"]].dtypes)

    return df


@st.cache_data()
def localizacao_coluna_medico(df):
    index = df.columns.get_loc("Médico Familia") - 3
    list_text = [
        "para_remover_2",
        "para_remover_3",
        "para_remover_4",
    ]

    list_text.insert(index, "Médico Familia")

    return list_text


@st.cache_data()
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
        df = df.reset_index(drop=True)

        nome_colunas = localizacao_coluna_medico(df)

        # #give name to columns
        df.columns = (
            ["Unidade", "para_remover_1", "id"]
            + nome_colunas
            + [
                "Numerador",
                "Denominador",
                "Valor",
            ]
        )

        # list_medicos = df["Médico Familia"].unique()
        # # replace the names of "Médico Familia" to a generic name "Médico 1"
        # for index, each in enumerate(list_medicos):
        #     df.loc[df["Médico Familia"] == each, "Médico Familia"] = f"Médico {index+1}"

        unidade = df["Unidade"].unique()[0]
        nome = f"{unidade} {mes}/{ano}"

        # drop column "Mês"
        df = df.drop(
            columns=[
                "Unidade",
                "para_remover_1",
                "para_remover_2",
                "para_remover_3",
                "para_remover_4",
            ]
        )

        # Uniformizar nomes de médicos
        df = medico(df, column="Médico Familia")

        # drop rows where "id" is Nan
        df = df.dropna(subset=["id"])

        # extrair id indicador
        df = extrair_id(df, "id")

        # remove lines that are exact duplicates and keep only one
        df = df.drop_duplicates()

        # make id the index
        df = df.set_index("id")

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

        df = df.reset_index(drop=True)

        # fill NA
        # df["Valor"] = df["Valor"].fillna(0)
        # df["Denominador"] = df["Denominador"].fillna(0)
        # df["Numerador"] = df["Numerador"].fillna(0)

        df["Valor"] = (
            df["Valor"]
            .apply(
                lambda x: x.replace(".", "").replace(",", ".")
                if isinstance(x, str)
                else x
            )
            .astype(float)
        )
        df["Numerador"] = (
            df["Numerador"]
            .apply(
                lambda x: x.replace(".", "").replace(",", ".")
                if isinstance(x, str)
                else x
            )
            .astype(float)
        )
        df["Denominador"] = (
            df["Denominador"]
            .apply(
                lambda x: x.replace(".", "").replace(",", ".")
                if isinstance(x, str)
                else x
            )
            .astype(float)
        )

        # drop lines were "Médico Familia" is Sem Médico
        # df = df[df["Médico Familia"] != "Sem Médico"]

        # sort by id
        df = df.sort_values("id")

        # score calculado a partir do valor do indicador e dos intervalos aceitável e esperado
        # se acima do máximo aceitave ou abaixo do mínimo aceitavel, score = 0
        # se entre o minimo e maxio esperado, score = 2
        # se entre minimo aceitabel e minimo esperado ou entre maximo esperado e maximo aceitavel, score = 1
        # se acima do maximo esperado mas abaico do maximo aceitavel, score = 1
        # valores aceitáveis e esperados estão noutra coluna e deve ser usados o da mesma linha

        df["Score"] = df.apply(calculate_score_mimuf, axis=1)

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

        # df.loc[df["Nome"] != "IDE"] = df.loc[df["Nome"] != "IDE"].fillna(0)

        # rename columns to remove year
        # df.rename(columns=lambda x: re.sub(r" 2023", "", x), inplace=True)

        df["Denominador"] = df["Denominador"].astype(float)
        df["Numerador"] = df["Numerador"].astype(float)

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


@st.cache_data()
def extracao_areas_clinicas(df):
    return df["Área clínica"].unique().tolist()
