import pandas as pd
from datetime import datetime
from ..utils import createDataframe, inputValueColumns, validDf

def bv(df):

    data = datetime.now().strftime("%d/%m/%Y")

    df = pd.read_excel(df)

    infos ={
       "NUM_PROPOSTA":"NUM_PROPOSTA",
       "NUM_CONTRATO":"NUM_CONTRATO",
       "VAL_LIQUIDO": "VAL_BASE_COMISSAO",
       "VAL_COMISSAO":"VAL_COMISSAO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    valores_tratados = []

    for valor in df_novo["VAL_BASE_COMISSAO"]:

        valor_str = valor

        if type(valor) == str:

            valor_str = str(valor)
            valor_teste = valor_str.replace("R$", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_teste = valor_teste.strip()
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_BASE_COMISSAO"] = valores_tratados

    valores_tratados = []


    for valor in df_novo["VAL_COMISSAO"]:

        valor_str = valor

        if type(valor) == str:

            valor_str = str(valor)
            valor_teste = valor_str.replace("R$", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_teste = valor_teste.strip()
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_COMISSAO"] = valores_tratados
    df_novo["DAT_CREDITO"] = data
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"] * 100)
    df_novo["NUM_BANCO"] = 44
    df_novo["NOM_BANCO"] = 'BV'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    return df_novo