import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def phtech(df):

    df = pd.read_csv(df, sep=";")

    infos ={
       "COD. BANCO":"NUM_PROPOSTA",
       "DATA PG. CORRETOR":"DAT_CREDITO",
       "VALOR LIQUIDO":"VAL_BASE_COMISSAO",
       "COMISSAO":"VAL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NUM_BANCO"] = 8768
    df_novo["NOM_BANCO"] = "PHTECH"
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo