import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from ..utils import createDataframe, inputValueColumns, validDf

def nyc(df):

    df = pd.read_excel(df, header=1)
    df = df.iloc[:-2]

    infos ={
       "Id":"NUM_PROPOSTA",
       "DataFinalização":"DAT_CREDITO",
       "ValorLiquido":"VAL_BASE_COMISSAO",
       "Valor Comissão Líquida":"VAL_COMISSAO",
       "% Comissão Líquida":"PCL_COMISSAO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NUM_BANCO"] = '1728'
    df_novo["NOM_BANCO"] = 'NYC BANK'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    return df_novo