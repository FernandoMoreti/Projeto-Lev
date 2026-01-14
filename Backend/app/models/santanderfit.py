import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def santanderfit(df):

    df = pd.read_excel(df, header=1)

    infos ={
        "Nº da Instalação":"NUM_PROPOSTA",
        "Valor a Receber":"VAL_COMISSAO",
        "Percentual (%)":"PCL_COMISSAO",
        "Valor Base (R$)":"VAL_BASE_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    valores_tratados = []

    for valor in df_novo["VAL_BASE_COMISSAO"]:

        valor_str = str(valor)

        valor_teste = valor_str.replace(".", "")
        valor_teste = valor_teste[:3] + "." + valor_teste[3:]
        print(valor_teste)
        valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_BASE_COMISSAO"] = valores_tratados

    valores_tratados = []

    for valor in df_novo["VAL_COMISSAO"]:

        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            print(valor_str)

            valor_teste = valor_str.replace("R$ ", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_COMISSAO"] = valores_tratados

    df_novo["NOM_BANCO"] = "FIT ECONOMIA DE ENERGIA S.A."
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["NUM_BANCO"] = 9173
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo