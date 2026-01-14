import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def vctex(df):


    df = pd.read_csv(df, sep=";")

    infos ={
       "Número do Contrato":"NUM_PROPOSTA",
       "Valor Liberado":"VAL_BASE_COMISSAO",
       "Data de Repasse Comissão": "DAT_CREDITO",
       "Valor Comissão":"VAL_COMISSAO",
       "% Comissão":"PCL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["NUM_BANCO"] = 1530
    df_novo["NOM_BANCO"] = "VCTEX CORRESPONDENTE"
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo