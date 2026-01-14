import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import requests
from ..utils import createDataframe, inputValueColumns, validDf

def queromaiscancelados(df):

    df = pd.read_excel(df)

    infos = {
       "CONTRATO":"NUM_PROPOSTA",
       "Valor Prêmio":"VAL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    list_val_bruto = []

    for prop in df_novo["NUM_PROPOSTA"]:
        data = requests.get(f"http://192.168.1.252:3004/v1/wb-api/proposta/?proposal={prop}")
        if data:
            result = data.json()
            list_val_bruto.append(result[0]["bruto"])

    df_novo["VAL_BRUTO"] = list_val_bruto

    valores_tratados = []

    for valor in df_novo["VAL_BRUTO"]:

        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_BRUTO"] = valores_tratados

    df_novo["NUM_BANCO"] = 3030
    df_novo["NOM_BANCO"] = 'QUERO MAIS CREDITO'
    df_novo["DAT_CREDITO"] = datetime.now().date()
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BRUTO"]
    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BRUTO"]
    df_novo["PCL_COMISSAO"] = df_novo["VAL_COMISSAO"] / df_novo["VAL_BRUTO"] * 100
    df_novo["TIPO_COMISSAO_BANCO"] = 'ESTORNO'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    return df_novo