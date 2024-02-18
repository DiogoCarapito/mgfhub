import pandas as pd


def extrair_id(df, coluna):
    # extrair o id que se econtra entre dois . (pontos) e transformar em int
    # exemplo de input: "2013.001.01 FL" output 1
    return df[coluna].str.extract(r"\.(\d+)\.", expand=False).astype(int)


def etl_bicsp(list_of_files):
    if list_of_files is None:
        return None

    list_of_dfs = [pd.read_excel(each, engine="openpyxl") for each in list_of_files]

    dict_dfs = {}

    for df in list_of_dfs:
        # processamento se  o ficherio tiver cabeçalho (summarized e underalying data)
        first_column_name = df.columns[0]
        if first_column_name.startswith("Applied"):
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

        unidade = "USF Maravilha"

        nome = f"{unidade} {ano}/{mes}"

        df["cor"] = df["Score"].apply(
            lambda x: "green" if x == 2 else ("red" if x == 0 else "yellow")
        )

        # Update list_of_dfs with the new df
        dict_dfs[nome] = {
            "data": df[["id", "Resultado", "Score", "cor"]],
            "ano": int(ano),
            "mes": int(mes),
            "unidade": unidade,
        }

    return dict_dfs
