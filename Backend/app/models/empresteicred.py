import pandas as pd
from datetime import datetime
from ..utils import createDataframe, inputValueColumns, validDf

def empresteicred(df):

    df = pd.read_excel(df)

    infos = {
        "Op": "NUM_PROPOSTA",
        "Líquido": "VAL_BASE_COMISSAO",
        "% Comissão": "PCL_COMISSAO",
        "Comissão": "VAL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    length = len(df_novo["NUM_PROPOSTA"])
    df_novo = df_novo.drop(df_novo.index[length-1])

    df_novo["NUM_BANCO"] = '1708'
    df_novo["NOM_BANCO"] = 'EMPRESTEI CARD'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["DAT_CREDITO"] = datetime.now().date()
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100

    return df_novo


