import pandas as pd
import os


def pre_process_sdm(source):
    # read csv
    df = pd.read_csv("./data/" + source)

    # make id the index
    # df.set_index("id", inplace=True)

    # save  original to ./data folder
    df.to_csv("./data/original_" + source)

    # search_indexes
    df["search_indexes"] = (
        df["id"].astype(str)
        + " "
        + df["Nome abreviado"]
        + " "
        + df["Designação"]
        + " "
        # + df["Descrição do Indicador"]
        # + " "
        + df["Área clínica"]
        + " "
        + df["Área | Subárea | Dimensão"]
    )
    # df["id"].astype(str) + " " +

    df["search_indexes"] = df["search_indexes"].str.lower()

    # remove accents
    df["search_indexes"] = (
        df["search_indexes"]
        .str.normalize("NFKD")
        .str.encode("ascii", errors="ignore")
        .str.decode("utf-8")
    )

    df["link_sdm"] = "https://sdm.min-saude.pt/BI.aspx?id=" + df["id"].astype(str)
    # + df["id"].astype(str)

    # drop columns
    df.drop(
        columns=[
            "Código SIARS",
            # "Nome abreviado",
            "Objetivo",
            # "Descrição do Indicador",
            "Regras de cálculo",
            "Observações Gerais",
            "Observações Sobre Software",
            "Período em Análise",
            "Fórmula",
            "Unidade de medida",
            "Output",
            "Estado do indicador",
            "Tipo de Indicador",
            "Inclusão de utentes no indicador",
            "Prazo para Registos",
        ],
        inplace=True,
    )

    # change column names
    df.rename(
        columns={
            "anos_disponiveis": "Anos Disponíveis",
            "aceitavel_2023": "Intervalo Aceitável 2023",
            "min_aceitavel_2023": "Mínimo Aceitável 2023",
            "max_aceitavel_2023": "Máximo Aceitável 2023",
            "aceitavel_2024": "Intervalo Aceitável 2024",
            "min_aceitavel_2024": "Mínimo Aceitável 2024",
            "max_aceitavel_2024": "Máximo Aceitável 2024",
            "esperado_2023": "Intervalo Esperado 2023",
            "min_esperado_2023": "Mínimo Esperado 2023",
            "max_esperado_2023": "Máximo Esperado 2023",
            "esperado_2024": "Intervalo Esperado 2024",
            "min_esperado_2024": "Mínimo Esperado 2024",
            "max_esperado_2024": "Máximo Esperado 2024",
        },
        inplace=True,
    )

    # add new column bicsp to indicate if the indicador is in bicsp 128 list
    df["bicsp"] = df["id"].isin(
        pd.read_csv("./data/indicadores_bicsp.csv", header=None)[0]
    )

    # transform ide and idg from 1 or 0/nan to True or False
    df["ide"] = df["ide"].apply(lambda x: True if x == 1 else False)
    df["idg"] = df["idg"].apply(lambda x: True if x == 1 else False)

    # save to ./data folder
    df.to_csv(f"./data/{source}")

    print(f"{source} pre-processed successfully!")


def pre_process_portaria_sunburst(source):
    # read csv
    df = pd.read_csv("./data/" + source)

    df_sdm = pd.read_csv("./data/indicadores_sdm_complete.csv")

    df = df.merge(
        df_sdm[
            [
                "id",
                "Nome abreviado",
                "Anos Disponíveis",
                "Intervalo Aceitável 2023",
                "Mínimo Aceitável 2023",
                "Máximo Aceitável 2023",
                "Intervalo Aceitável 2024",
                "Mínimo Aceitável 2024",
                "Máximo Aceitável 2024",
                "Intervalo Esperado 2023",
                "Mínimo Esperado 2023",
                "Máximo Esperado 2023",
                "Intervalo Esperado 2024",
                "Mínimo Esperado 2024",
                "Máximo Esperado 2024",
            ]
        ],
        on="id",
        how="left",
    )

    # get the unique values of the columns "Dimensão" and create a new lines for each one, where "Ponderaão"  is the sum of all the lines that have that "Dimensão"
    df_dimensao = df.groupby(["Dimensão"]).sum().reset_index()

    # make "Nome" the name of the "Dimensão"
    df_dimensao["Nome"] = df_dimensao["Dimensão"]

    # remove the values of the columns that dont make sense
    df_dimensao[
        [
            "Dimensão",
            "id",
            "Intervalo esperado",
            "Intervalo aceitável",
            "min_esperado",
            "max_esperado",
            "min_aceitavel",
            "max_aceitavel",
            "Nome abreviado",
        ]
    ] = None

    df_dimensao["Dimensão"] = "IDE"

    # add a new column "Lable" with the values of "Nome" for the "Dimensão" = "IDE"
    df_dimensao.loc[df_dimensao["Dimensão"] == "IDE", "Lable"] = df_dimensao["Nome"]

    # add a new column "Lable" with the values of "id" for the "Dimensão" != "IDE"
    df.loc[df["Dimensão"] != "IDE", "Lable"] = df["id"].astype(str)

    df["Nome"] = df["id"].astype(str) + " - " + df["Nome abreviado"]
    # df["Nome"] = df["Nome abreviado"]

    # Contact
    # Exclude empty or all-NA columns
    df_dimensao = df_dimensao.dropna(axis=1, how="all")
    df = df.dropna(axis=1, how="all")
    # Append the two dataframes
    df = pd.concat([df_dimensao, df], ignore_index=True)

    # add a new row wirh Nome = "IDE" with all blank values
    new_row = pd.DataFrame(
        {
            "Nome": ["IDE"],
            "Dimensão": [None],
            "Lable": ["IDE"],
            "id": [None],
            "Ponderação": [100],
            "Intervalo esperado": [None],
            "Intervalo aceitável": [None],
            "min_esperado": [None],
            "max_esperado": [None],
            "min_aceitavel": [None],
            "max_aceitavel": [None],
            "Nome abreviado": [None],
        }
    )

    # Contact
    # Exclude empty or all-NA columns
    df = df.dropna(axis=1, how="all")
    new_row = new_row.dropna(axis=1, how="all")

    # Concatenate the dataframe and the new row
    df = pd.concat([df, new_row], ignore_index=True)

    # save to ./data folder
    df.to_csv(f"./data/sunburst_{source}", index=False)

    print(f"{source} pre-processed successfully!")


def download_update_data(source):
    # url from github's datasets_indicadores repo
    url = f"https://github.com/DiogoCarapito/datasets_indicadores/raw/main/datasets/{source}"

    # read csv and save to ./data folder
    df = pd.read_csv(url, index_col=0)
    df.to_csv("./data/" + source)

    # success message
    print(f"{source} saved successfully!")


def bicsp_list_indicadores():
    from utils.etl_relatorios import extrair_id

    # open excel file
    df = pd.read_excel("./offline_data/bicsp.xlsx", engine="openpyxl")

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

    # sort by id
    df.sort_values("id", inplace=True)

    df = df["id"]

    df.to_csv("./data/indicadores_bicsp.csv", index=False, header=False)

    # success message
    print("indicadores_bicsp.csv saved successfully!")


def delete_file(file_path):
    os.remove(file_path)
    print(f"{file_path} deleted successfully!")


def complete_sunburst_portaria_411a_2023():
    df = pd.read_csv("./data/sunburst_portaria_411a_2023.csv")

    # if there isnt a column "Área clínica" add it
    if "Área clínica" in df.columns:
        # remove the column "Área clínica"
        df.drop(columns=["Área clínica"], inplace=True)

    # get the data from indicadores_sdm_complete.csv and make "Área clínica" correspond to the id
    df_sdm = pd.read_csv("./data/indicadores_sdm_complete.csv")
    df_sdm = df_sdm[["id", "Área clínica"]]
    df = df.merge(df_sdm, on="id", how="left")

    # save to ./data folder
    df.to_csv("./data/sunburst_portaria_411a_2023.csv", index=False)


if __name__ == "__main__":
    # download/update all data
    # main csv file with all indicadores
    download_update_data("indicadores_sdm_complete.csv")

    # list of IDE indicadores
    download_update_data("indicadores_ide.csv")

    # list of IDG indicadores
    download_update_data("indicadores_idg.csv")

    # download dados portaria 411a 2023
    download_update_data("portaria_411a_2023.csv")

    # bicsp_list_indicadores()

    # pre-processed data for table
    pre_process_sdm("indicadores_sdm_complete.csv")

    # create sunburst data for ide
    pre_process_portaria_sunburst("portaria_411a_2023.csv")

    # remover o original
    delete_file("data/original_indicadores_sdm_complete.csv")

    # add area clinica to sunburst_portaria_411a_2023.csv
    complete_sunburst_portaria_411a_2023()
