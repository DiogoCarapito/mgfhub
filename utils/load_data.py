import pandas as pd

def pre_process(source):
    # read csv
    df = pd.read_csv("./data/" + source)
    
    #make id the index
    #df.set_index("id", inplace=True)
   
    # save  original to ./data folder
    df.to_csv("./data/original_" + source)
    
    #search_indexes
    df["search_indexes"] = df["id"].astype(str) + " " + df["Nome abreviado"] + " " + df["Designação"] + " " + df["Descrição do Indicador"] + " " + df["Área clínica"] + " " + df["Área | Subárea | Dimensão"]
    # df["id"].astype(str) + " " +
    
    df["link_sdm"] = "https://sdm.min-saude.pt/BI.aspx?id=" + df["id"].astype(str)
    #+ df["id"].astype(str)
    
    # drop columns
    df.drop(
        columns=[
            "Código SIARS",
            "Nome abreviado",
            "Objetivo",
            "Descrição do Indicador",
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
            "Prazo para Registos"
        ], inplace=True,
    )

    # save to ./data folder
    return df.to_csv("./data/" + source)
    

def download_update_data(source):
    # url from github's datasets_indicadores repo
    url = f"https://github.com/DiogoCarapito/datasets_indicadores/raw/main/datasets/{source}"

    # read csv and save to ./data folder
    df = pd.read_csv(url, index_col=0)
    df.to_csv("./data/" + source)

    # success message
    print(f"{source} saved successfully!")


if __name__ == "__main__":
    # download/update all data
    # main csv file with all indicadores
    download_update_data("indicadores_sdm_complete.csv")

    # list of IDE indicadores
    download_update_data("indicadores_ide.csv")

    # list of IDG indicadores
    download_update_data("indicadores_idg.csv")

    # pre-processed data for table
    pre_process("indicadores_sdm_complete.csv")
