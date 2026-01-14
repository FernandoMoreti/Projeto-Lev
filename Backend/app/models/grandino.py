import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def grandino(df):

    df = pd.read_csv(df, sep=";")

    infos ={
       "Nro Proposta":"NUM_PROPOSTA",
       "Data de Fechamento":"DAT_CREDITO",
       "Base de Cálculo":"VAL_BASE_COMISSAO",
       "Valor Comissão":"VAL_COMISSAO",
       "Porcentagem":"PCL_COMISSAO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["NUM_BANCO"] = '88888'
    df_novo["NOM_BANCO"] = 'GRANDINO LTDA'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    return df_novo