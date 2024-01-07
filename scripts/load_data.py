import pandas as pd

def upsave_data_source(source):
    url = "https://github.com/DiogoCarapito/datasets_indicadores/raw/main/datasets/indicadores_sdm.csv"
    df = pd.read_csv(url, index_col=0)
    df.to_csv("./data/" + source)
    print(f"{source} saved successfully!")
    
if __name__ == "__main__":
    upsave_data_source("indicadores_sdm.csv")