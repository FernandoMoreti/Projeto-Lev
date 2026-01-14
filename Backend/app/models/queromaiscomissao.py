import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from ..utils import createDataframe, inputValueColumns, validDf

def queromaiscomisssao(df):

    df = pd.read_excel(df)

    infos = {
       "NR.PROP.":"NUM_PROPOSTA",
       "VLR TOTAL PRODUCUÇÃO (VLR LIQUIDO + SEGURO)":"VAL_BASE_COMISSAO",
       "Valor Comissão":"VAL_COMISSAO",
       "% Comissão":"PCL_COMISSAO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NUM_BANCO"] = 3030
    df_novo["NOM_BANCO"] = 'QUERO MAIS CREDITO'
    df_novo["DAT_CREDITO"] = datetime.now().date()
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    return df_novo