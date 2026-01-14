import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def euro(df):

    df = pd.read_excel(df)

    infos = {
        "Proposta":"NUM_PROPOSTA",
        "Vlr. Liberado":"VAL_BASE_COMISSAO",
        "% Comissão":"PCL_COMISSAO",
        "Vlr. Comissão":"VAL_COMISSAO",
        "Dt. de Pagamento":"DAT_CREDITO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    tamanho = len(df_novo["NUM_PROPOSTA"])

    df_novo = df_novo.drop(index=[tamanho -1, tamanho -2])

    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(str).str.replace("%", "").astype(float)
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["NUM_BANCO"] = "359108"
    df_novo["NOM_BANCO"] = "EURO17 EMPRESARIAL"

    return df_novo