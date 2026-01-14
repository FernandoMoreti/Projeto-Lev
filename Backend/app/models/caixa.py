import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf


def caixa(df):

    df = pd.read_excel(df)

    infos ={
        "Nr Proposta":"NUM_PROPOSTA",
        "Valor Liberado Cliente":"VAL_BASE_COMISSAO",
        "% Comissao":"PCL_COMISSAO",
        "Valor Nota Fiscal":"VAL_COMISSAO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NOM_BANCO"] = "CAIXA"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["NUM_BANCO"] = 104
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100
    return df_novo