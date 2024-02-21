import pandas as pd
import re

import streamlit as st

from mimufs.processing import medico


def extrair_id(df, coluna):
    # extrair o id que se econtra entre dois . (pontos) e transformar em int
    # exemplo de input: "2013.001.01 FL" output 1
    return df[coluna].str.extract(r"\.(\d+)\.", expand=False).astype(int)


def etiqueta_ano(df, ano):
    # cria as etiquetas para os intervalos aceitáveis e esperados com o ano correcto correspondente aos dados extraídos

    int_aceit = f"Intervalo Aceitável {ano}"
    int_esper = f"Intervalo Esperado {ano}"

    # caso não haja intervalos para o ano dos dados, por definição usa os intervalos de 2023
    if int_aceit not in df.columns or int_esper not in df.columns:
        int_aceit = "Intervalo Aceitável 2023"
        int_esper = "Intervalo Esperado 2023"

    return int_aceit, int_esper


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

        df["Resultado"] = df["Resultado"].astype(float)
        df["Score"] = df["Score"].astype(float)

        # Update list_of_dfs with the new df
        dict_dfs[nome] = {
            "data": df[["id", "Resultado", "Score", "Mês Ind"]],
            "nome": nome,
            "ano": int(ano),
            "mes": int(mes),
            "unidade": unidade,
        }

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

        st.write(df.columns.shape[0] == 10)

        ano_mes = df.columns[7]
        ano = ano_mes[:4]
        mes = ano_mes[5:7]
        unidade = "TOP"
        nome = f"{unidade} {mes}/{ano}"

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

        # drop column "Mês"
        df.drop(
            columns=[
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


        
        # get sunburst_portaria csv
        df_portaria = pd.read_csv("./data/sunburst_portaria_411a_2023.csv")
        
        colunas_portaria = [
            "id",
            "Nome",
            "Dimensão",
            "Ponderação",
            
            "Intervalo Aceitável 2023",
            "Mínimo Aceitável 2023",
            "Máximo Aceitável 2023",
            
            "Intervalo Esperado 2023",
            "Mínimo Esperado 2023",
            "Máximo Esperado 2023",            
            
            "Intervalo Aceitável 2024",
            "Mínimo Aceitável 2024",
            "Máximo Aceitável 2024",

            "Intervalo Esperado 2024",
            "Mínimo Esperado 2024",
            "Máximo Esperado 2024",
        ]
        
        # merge df with df_portaria
        df = df.merge(
            df_portaria[colunas_portaria],
            on="id",
            how="right",
        )
        # drop rows with NaN
        df.dropna(subset=["Unidade"], inplace=True)
        
                # save as a dictionary name:df
        dict_dfs[nome] = {
            "df": df,
            "ano": ano,
            "mes": mes,
            "unidade": unidade,
            "nome": nome,
        }

    return dict_dfs
