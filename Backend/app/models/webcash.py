import pandas as pd
from datetime import datetime
from ..utils import createDataframe, inputValueColumns, validDf

def webcash(df):

    df = pd.read_excel(df)
    data = datetime.now().strftime("%d/%m/%Y")

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "SEGURO":"VAL_BRUTO",
       "LIQUIDO":"VAL_LIQUIDO",
       "COMISSÃO":"VAL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BRUTO"] + df_novo["VAL_LIQUIDO"]
    df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100
    df_novo["NOM_BANCO"] = "WEBCASH"
    df_novo["NUM_BANCO"] = 1730
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["DAT_CREDITO"] = data
    df_novo["VAL_LIQUIDO"] = ""
    df_novo["VAL_BRUTO"] = ""

    return df_novo

