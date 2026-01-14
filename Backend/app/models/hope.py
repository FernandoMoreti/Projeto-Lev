import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def hope(df):

    df = pd.read_html(df, header=0)[0]

    infos ={
        "Número Ade":"NUM_PROPOSTA",
        "Data do Fechamento":"DAT_CREDITO",
        "Valor Bruto":"VAL_BASE_COMISSAO",
        "% Comissão": "PCL_COMISSAO",
        "Valor":"VAL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    tamanho = len(df_novo["NUM_PROPOSTA"])
    df_novo = df_novo.drop(df_novo.index[tamanho-1])
    df_novo = df_novo.drop(df_novo.index[tamanho-2])


    valores_tratados = []

    for valor in df_novo["VAL_BASE_COMISSAO"]:

        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)
            valor_teste = valor_str.replace("R$ ", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_BASE_COMISSAO"] = valores_tratados

    df_novo["NOM_BANCO"] = "HOPE"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] / 100 * df_novo["PCL_COMISSAO"]
    df_novo["NUM_BANCO"] = 1597
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo