import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from ..utils import createDataframe, inputValueColumns, validDf

def v8(df):

    df = pd.read_excel(df)

    infos ={
        "NUM_PROPOSTA":"NUM_PROPOSTA",
        "DAT_CREDITO":"DAT_CREDITO",
        "VAL_BASE_COMISSAO":"VAL_BASE_COMISSAO",
        "VAL_COMISSAO_TOTAL":"VAL_COMISSAO",
        "PERCENTUAL_REPASSE_TOTAL":"PCL_COMISSAO",
        "NUM_CONTRATO": "NUM_CONTRATO",
        "COD_PRODUTO" : "COD_PRODUTO",
        "DSC_PRODUTO" : "DSC_PRODUTO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    if"NUM_PROPOSTA"in df.columns:
        df["NUM_PROPOSTA"] = df["NUM_PROPOSTA"].astype(str)

    df_novo["NUM_BANCO"] = '1725'
    df_novo["NOM_BANCO"] = 'V8 DIGITAL'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'

    return df_novo