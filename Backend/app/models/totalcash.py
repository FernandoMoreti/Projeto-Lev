import pandas as pd
from datetime import datetime
import requests
from ..utils import createDataframe, inputValueColumns, validDf

def totalcash(df):
    df = pd.read_excel(df)

    infos = {
        "Nr Proposta": "NUM_PROPOSTA",
        "Valor Proposta": "VAL_BASE_COMISSAO",
        "Valor Comissão": "VAL_COMISSAO",
        "% Comissao": "PCL_COMISSAO",
        "Taxa Pagamento": "PCL_TAXA_EMPRESTIMO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    for index, row in df_novo.iterrows():
        if row["VAL_COMISSAO"] < 0:
            response = requests.get(f"http://192.168.1.252:3004/v1/wb-api/proposta/?proposal={row["NUM_PROPOSTA"]}")
            data = response.json()
            df_novo.at[index, "VAL_BASE_COMISSAO"] = data[0]["bruto"]
            df_novo.at[index, "TIPO_COMISSAO_BANCO"] = "ESTORNO"
        else:
            df_novo.at[index, "TIPO_COMISSAO_BANCO"] = "DIRETA"

    valores_tratados = []

    for valor in df_novo["VAL_BASE_COMISSAO"]:
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_BASE_COMISSAO"] = valores_tratados

    df_novo["NUM_BANCO"] = 1731
    df_novo["NOM_BANCO"] = "TOTALCASH"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["DAT_CREDITO"] = datetime.now().date()
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100

    return df_novo