import pandas as pd
from datetime import datetime
from ..utils import createDataframe, inputValueColumns, validDf

def neo(df):

    data = df.filename.split("_")[1].split(".")[0]
    resultado = f"{data[:2]}/{data[2:4]}/{data[4:]}"

    df = pd.read_excel(df)

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "VALOR BRUTO":"VAL_BASE_COMISSAO",
       "CMS R$":"VAL_COMISSAO",
       "CMS %":"PCL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    tamanho = len(df_novo)

    df_novo = df_novo.drop(index=[tamanho -1, tamanho -2, tamanho -3, tamanho -4])

    df_novo["PCL_COMISSAO"] = round(df_novo["PCL_COMISSAO"] * 100, 2)

    df_novo["NUM_BANCO"] = 3333333
    df_novo["NOM_BANCO"] = "NEO CREDITO"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["DAT_CREDITO"] = resultado

    return df_novo