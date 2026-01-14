import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def kardbank(df):

    df = pd.read_html(df, header=0)[0]

    infos ={
        "Número Ade":"NUM_PROPOSTA",
        "Data Pgto Vendedor":"DAT_CREDITO",
        "Valor Bruto":"VAL_BASE_COMISSAO",
        "% Comissão":"PCL_COMISSAO",
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
            valor_teste = valor_str.replace("R$ ", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_BASE_COMISSAO"] = valores_tratados

    df_novo["NOM_BANCO"] = "KARDBANK"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] * (df_novo["PCL_COMISSAO"] / 100)
    df_novo["NUM_BANCO"] = 6910
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo