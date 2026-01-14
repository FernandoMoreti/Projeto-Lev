import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def evol(df):

    df = pd.read_excel(df)

    infos ={
        "Id_Operation":"NUM_PROPOSTA",
        "Taxa":"PCL_TAXA_EMPRESTIMO",
        "Valor_Liberado":"VAL_LIQUIDO",
        "Comissão":"VAL_COMISSAO",
        "Valor_Bruto":"VAL_BRUTO",
        "Data de Pagamento Comissão":"DAT_CREDITO",
        "Percentual_Comissao":"PCL_COMISSAO",
        "Descricao_Tipo_Operacao" :"DSC_TIPO_PROPOSTA_EMPRESTIMO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    for index, row in df_novo.iterrows():
        if row["DSC_TIPO_PROPOSTA_EMPRESTIMO"] == "PORT + REFIN - NORMAL":
            df_novo.at[index, "VAL_BASE_COMISSAO"] = row["VAL_BRUTO"]
        else:
            df_novo.at[index, "VAL_BASE_COMISSAO"] = row["VAL_LIQUIDO"]

    df_novo["NOM_BANCO"] = "EVOL"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["NUM_BANCO"] = 7777
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["DSC_TIPO_PROPOSTA_EMPRESTIMO"] = None

    return df_novo