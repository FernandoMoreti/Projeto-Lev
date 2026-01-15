import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def c6auto(df):
    df = pd.read_excel(df)

    infos = {
        "Contrato": "NUM_PROPOSTA",
        "Dt. Produção Date": "DAT_CREDITO",
        "Vlr. Principal Base": "VAL_BASE_COMISSAO",
        "% de Comissão Total": "PCL_COMISSAO",
        "Vlr. Líquido": "VAL_COMISSAO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NUM_BANCO"] = 3336
    df_novo["NOM_BANCO"] = 'C6 AUTO'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100

    return df_novo