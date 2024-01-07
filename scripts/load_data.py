import pandas as pd


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
