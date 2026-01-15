import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def bmgseguro(df):
    df = pd.read_csv(df, sep=";")

    infos = {
        "Data Pagamento": "DAT_CREDITO",
        "Adesao": "NUM_PROPOSTA",
        "Valor Base": "VAL_BASE_COMISSAO",
        "Valor Bruto": "VAL_COMISSAO",
        "% de Comissao": "PCL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NOM_BANCO"] = "BANCO BMG S.A."
    df_novo["NUM_BANCO"] = 318
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSOA_BANCO"] = "SEGURO"
    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)

    return df_novo