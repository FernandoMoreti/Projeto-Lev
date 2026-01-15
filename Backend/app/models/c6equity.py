import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def c6equity(df):
    df = pd.read_excel(df)

    infos = {
        "CD CONTRATO": "NUM_PROPOSTA",
        "DT PRODUÇÃO": "DAT_CREDITO",
        "VL PRINCIPAL": "VAL_BASE_COMISSAO",
        "PC COMISSAO FLAT": "PCL_COMISSAO",
        "VALOR COMISSAO": "VAL_COMISSAO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NUM_BANCO"] = 336
    df_novo["NOM_BANCO"] = 'C6 BANK'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100

    return df_novo