import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def icred(df):

    df = pd.read_excel(df)

    infos ={
       "Number":"NUM_PROPOSTA",
       "Data":"DAT_CREDITO",
       "commission_base":"VAL_BASE_COMISSAO",
       "commission_factor": "PCL_COMISSAO",
       "commission_value":"VAL_COMISSAO",
       "commission_type":"TIPO_COMISSAO_BANCO"
    }
    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["NUM_BANCO"] = '329'
    df_novo["NOM_BANCO"] = 'ICRED'
    df_novo["TIPO_COMISSAO_BANCO"] = df_novo["TIPO_COMISSAO_BANCO"].replace('Flat', 'DIRETA')
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    return df_novo