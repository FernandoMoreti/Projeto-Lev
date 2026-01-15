import pandas as pd
import requests

def facta(df):
    df = pd.read_excel(df)

    list_prop = []

    for index, row in df.iterrows():
        if "PGTO ADIANTAMENTO" in row["OBSERVACAO"]:
            list_prop.append(row["CODIGOAF"])

    list_val_bruto = []
    new_list_prop = []

    for proposal in list_prop:
        data = requests.get(f"http://192.168.1.252:3004/v1/wb-api/proposta/?proposal={proposal}", timeout=5)
        if data and data.status_code == 200:
            result = data.json()
            list_val_bruto.append(result[0]["bruto"])
            new_list_prop.append(proposal)

    print(new_list_prop)
    print(list_val_bruto)

    for index, row in df.iterrows():
        if row["CODIGOAF"] in new_list_prop and "PGTO ADIANTAMENTO" in row["OBSERVACAO"]:
            pos = new_list_prop.index(row["CODIGOAF"])
            df.at[index, "VLRAF"] = list_val_bruto[pos]

    valores_tratados = []

    for valor in df["VLRAF"]:
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df["VLRAF"] = valores_tratados

    return df