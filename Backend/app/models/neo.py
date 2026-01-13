import pandas as pd
from datetime import datetime

def neo(df, cols_opcoes):

    data = df.filename.split("_")[1].split(".")[0]
    resultado = f"{data[:2]}/{data[2:4]}/{data[4:]}"

    df = pd.read_excel(df)

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "VALOR BRUTO":"VAL_BASE_COMISSAO",
       "CMS R$":"VAL_COMISSAO",
       "CMS %":"PCL_COMISSAO",       
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"
    
    df_novo = pd.DataFrame(columns=cols_opcoes)

    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    tamanho = len(df_novo)

    df_novo = df_novo.drop(index=[tamanho -1, tamanho -2, tamanho -3, tamanho -4])

    df_novo["PCL_COMISSAO"] = round(df_novo["PCL_COMISSAO"] * 100, 2)

    df_novo["NUM_BANCO"] = 3333333
    df_novo["NOM_BANCO"] = "NEO CREDITO"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["DAT_CREDITO"] = resultado

    return df_novo