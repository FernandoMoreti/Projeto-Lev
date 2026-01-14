import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def aki(df):

    data = df.filename.split("_")[0]
    diaMesAno = f"{data[:2]}/{data[3:5]}/{data[6:]}"

    df = pd.read_excel(df)

    infos = {
        "Nº Contrato": "NUM_PROPOSTA",
        "Valor Total": "VAL_BASE_COMISSAO",
        "% Comissão": "PCL_COMISSAO",
        "Valor Comissão": "VAL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100
    df_novo["DAT_CREDITO"] = diaMesAno
    df_novo["NUM_BANCO"] = 1684
    df_novo["NOM_BANCO"] = "AKI CAPITAL"

    return df_novo
