import pandas as pd

def c6bankcomissao(df):
    df = pd.read_excel(df)

    validNames = ["PACOTE"]

    for i, row in df.iterrows():
        if row["Nome Comissionado"] != "LEV":
            df.at[i, "Vlr Bruto"] = 0

        if any(name in row["Possui Pacote/Seguro?"] for name in validNames) and row["Possui Pacote/Seguro?"] != "SEM PACOTE":
            df.at[i, "Tabela Cod Desc"] = None
            df.at[i, "Cod Produto"] = 0

    return df