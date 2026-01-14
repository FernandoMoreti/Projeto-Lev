import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from ..utils import createDataframe, inputValueColumns, validDf

def queromaisseguro(df):

    df = pd.read_excel(df, header=4)

    infos = {
       "Contrato":"NUM_PROPOSTA",
       "VALOR DE SEGURO":"VAL_BASE_COMISSAO",
       "OBS":"DSC_OBSERVACAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    for row in df_novo.itertuples():
        print(row.DSC_OBSERVACAO)
        if pd.isna(row.DSC_OBSERVACAO):
            df_novo.at[row.Index, "TIPO_COMISSAO_BANCO"] = 'SEGURO'
        else:
            df_novo.at[row.Index, "TIPO_COMISSAO_BANCO"] = 'ESTORNO SEGURO'

    df_novo["NUM_BANCO"] = 3030
    df_novo["NOM_BANCO"] = 'QUERO MAIS CREDITO'
    df_novo["DAT_CREDITO"] = datetime.now().date()
    df_novo["PCL_COMISSAO"] = 30
    df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] * 0.3
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    return df_novo