import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def grandino(df):

    df = pd.read_csv(df, sep=";")

    infos ={
       "Nro Proposta":"NUM_PROPOSTA",
       "Data de Fechamento":"DAT_CREDITO",
       "Base de Cálculo":"VAL_BASE_COMISSAO",
       "Valor Comissão":"VAL_COMISSAO",
       "Porcentagem":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '88888'
    df_novo["NOM_BANCO"] = 'GRANDINO LTDA'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    return df_novo