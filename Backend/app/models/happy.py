import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def happy(df):

    df = pd.read_excel(df, header=2)

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "DT PAGTO":"DAT_CREDITO",
       "VR BASE":"VAL_BASE_COMISSAO",
       "VR CMS":"VAL_COMISSAO",
       "% CMS":"PCL_COMISSAO",
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

    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["NUM_BANCO"] = 1010
    df_novo["NOM_BANCO"] = 'HAPPY'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    for i in range(len(df_novo["VAL_BASE_COMISSAO"])):
        if df_novo["VAL_BASE_COMISSAO"][i] < 0:
            df_novo.loc[i, "TIPO_COMISSAO_BANCO"] = 'ESTORNO'
        else:
            df_novo.loc[i, "TIPO_COMISSAO_BANCO"] = 'DIRETA'

    return df_novo