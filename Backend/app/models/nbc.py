import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def nbc(df):
    df = pd.read_excel(df, header=10)

    infos = {
        "Nr. Proposta": "NUM_PROPOSTA",
        "Base de Cálculo": "VAL_BASE_COMISSAO",
        "Valor da Comissão": "VAL_COMISSAO",
        "Percentual": "PCL_COMISSAO",
        "Data Base": "DAT_CREDITO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    length = len(df_novo["NUM_PROPOSTA"])
    df_novo = df_novo.drop(df_novo.index[length-1])
    df_novo = df_novo.drop(df_novo.index[length-2])
    df_novo = df_novo.drop(df_novo.index[length-3])

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

    valores_tratados = []

    for valor in df_novo["VAL_COMISSAO"]:
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_COMISSAO"] = valores_tratados

    valores_tratados = []

    for valor in df_novo["PCL_COMISSAO"]:
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["PCL_COMISSAO"] = valores_tratados


    df_novo["NUM_BANCO"] = 753
    df_novo["NOM_BANCO"] = "NBC BANK"
    df_novo["NUM_PROPOSTA"] = df_novo["NUM_PROPOSTA"].astype(int)
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo