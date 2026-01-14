import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def qualibank(df):

    df = pd.read_excel(df)

    infos ={
       "NUMERO_CTT":"NUM_PROPOSTA",
       "DATA_PAGAMENTO":"DAT_CREDITO",
       "VALOR_BASE":"VAL_BASE_COMISSAO",
       "VALOR_INCENTIVO":"VAL_COMISSAO",
       "PERC_INCENTIVO":"PCL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NUM_BANCO"] = 2222222
    df_novo["NOM_BANCO"] = "QUALI BANK"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo