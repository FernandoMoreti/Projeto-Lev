import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def safracomissaozero(df):
    df = pd.read_csv(df, sep=';')

    infos = {
        "Contrato": "NUM_PROPOSTA",
        "Valor Principal": "VAL_BASE_COMISSAO",
        "Data efetivacao Contrato": "DAT_CREDITO",
        "CPF": "COD_CPF_CLIENTE",
        "Nome Cliente": "NOM_CLIENTE",
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

    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["NOM_BANCO"] = "Safra"
    df_novo["NUM_BANCO"] = 42
    df_novo["TIPO_COMISSAO_BANCO"] = "AUTORREGULAÇAO"

    return df_novo