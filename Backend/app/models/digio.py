import pandas as pd
from datetime import datetime
from ..utils import createDataframe, inputValueColumns, validDf

def digio(df):

    df = pd.read_csv(df, sep=";")

    infos = {
        "Prop.": "NUM_PROPOSTA",
        "Base de Cálculo": "VAL_BASE_COMISSAO",
        "Valor Comiss": "VAL_COMISSAO",
        "Parâm": "PCL_COMISSAO",
        "Dt. Pgto Cmss.": "DAT_CREDITO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["NUM_BANCO"] = 335
    df_novo["NOM_BANCO"] = "BANCO DIGIO"
    df_novo["PCL_COMISSAO"] = (df_novo["PCL_COMISSAO"].astype(str).str.replace(",", ".").astype(float) * 100)

    return df_novo