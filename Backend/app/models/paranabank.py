import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def paranabank(df):
    df = pd.read_excel(df)

    infos = {
        "Nr. Proposta": "NUM_PROPOSTA",
        "Data Fatura": "DAT_CREDITO",
        "Valor base": "VAL_BASE_COMISSAO",
        "% Comissão": "PCL_COMISSAO",
        "Valor comissão": "VAL_COMISSAO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NUM_BANCO"] = 254
    df_novo["NOM_BANCO"] = "PARANÁ BANCO S.A."
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["NUM_BANCO"] = 254
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo