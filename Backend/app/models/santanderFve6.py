import pandas as pd
from datetime import datetime, date, timedelta
from ..utils import createDataframe, inputValueColumns, validDf

def santanderfvevi(df):

    df = pd.read_csv(df, sep=";")

    infos = {
        "Proposta": "NUM_PROPOSTA",
        "Valor Bruto": "VAL_BASE_COMISSAO",
        "Percentual Comissão": "PCL_COMISSAO",
        "Valor Total Comissão": "VAL_COMISSAO",
        "Data do Cálculo": "DAT_CREDITO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["NUM_BANCO"] = 351
    df_novo["NOM_BANCO"] = "SANTANDER"
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo