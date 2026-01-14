import pandas as pd
from datetime import datetime
from ..utils import createDataframe, inputValueColumns, validDf

def jbcred(df):

    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")

    df = pd.read_html(df, header=0)[0]

    infos ={
        "NRCONTRATO":"NUM_PROPOSTA",
        "VLR_OPER":"VAL_BASE_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    num_propostas = []

    for num in df_novo["NUM_PROPOSTA"]:
        num_str = str(num)
        num_str = num_str.replace("-", "")
        num_str = float(num_str)
        num_propostas.append(num_str)

    df_novo["NUM_PROPOSTA"] = num_propostas
    df_novo["DAT_CREDITO"] = current_date
    df_novo["NOM_BANCO"] = "JBCRED"
    df_novo["PCL_COMISSAO"] = 10
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] / 10
    df_novo["NUM_BANCO"] = 777
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo