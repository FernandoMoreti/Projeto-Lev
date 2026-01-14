import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def santanderolewl(df):

    df = pd.read_csv(df, sep=";")

    infos ={
       "Proposta": "NUM_PROPOSTA",
       "Valor Líquido": "VAL_BASE_COMISSAO",
       "Valor Total Comissão": "VAL_COMISSAO",
       "Percentual Comissão": "PCL_COMISSAO",
       "Data do Cálculo": "DAT_CREDITO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

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

    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["NUM_BANCO"] = 218
    df_novo["NOM_BANCO"] = "BANCO OLE"

    return df_novo