import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
from ..utils import createDataframe, inputValueColumns, validDf

def presenca(df):

    df = pd.read_excel(df, header=2)

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "DT PAGTO":"DAT_CREDITO",
       "VR BASE":"VAL_BASE_COMISSAO",
       "VR CMS":"VAL_COMISSAO",
       "% CMS":"PCL_COMISSAO",
    }

    tamanho = len(df["PROPOSTA"])

    df = df.drop(index=[tamanho -1])

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str)
    mascara = df_novo["VAL_BASE_COMISSAO"].str.len() <= 6
    df_novo.loc[mascara, "VAL_BASE_COMISSAO"] = df_novo.loc[mascara, "VAL_BASE_COMISSAO"].str.replace(".", ",", regex=False)
    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].str.replace(".", "").str.replace(",", ".").astype(float)
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["NUM_BANCO"] = 482
    df_novo["NOM_BANCO"] = 'PRESENCA BANK SCP'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    for i in range(len(df_novo["VAL_BASE_COMISSAO"])):
        if df_novo["VAL_BASE_COMISSAO"][i] < 0:
            df_novo.loc[i, "TIPO_COMISSAO_BANCO"] = 'ESTORNO'
        else:
            df_novo.loc[i, "TIPO_COMISSAO_BANCO"] = 'DIRETA'

    return df_novo