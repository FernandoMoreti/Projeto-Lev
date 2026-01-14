import pandas as pd
from datetime import datetime, timedelta
from ..utils import createDataframe, inputValueColumns, validDf

def crefisa(df):

    df = pd.read_html(df, header=0)[0]

    print(df["Vlr_Pagamento_Comissao"])
    print(df["Vlr_Pagamento_Comissao"].dtype)

    infos ={
       "Num_Proposta":"NUM_PROPOSTA",
       "Data_Geracao_Comissao":"DAT_CREDITO",
       "Vlr_Liquido":"VAL_BASE_COMISSAO",
       "Vlr_Pagamento_Comissao":"VAL_COMISSAO",
       "Perc_Pagamento_Comissao":"PCL_COMISSAO",
       "Tipo":"TIPO_COMISSAO_BANCO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    for index, row in df_novo.iterrows():
        if row["TIPO_COMISSAO_BANCO"] == "À Vista":
            df_novo.at[index, "TIPO_COMISSAO_BANCO"] = "DIRETA"

    df_novo["NUM_BANCO"] = '69'
    df_novo["NOM_BANCO"] = 'BANCO CREFISA S.A.'
    df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(float) / 100
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    return df_novo