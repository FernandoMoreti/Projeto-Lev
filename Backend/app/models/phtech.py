import pandas as pd
import cols_opcoes

def phtech(df):

    df = pd.read_csv(df, sep=";")

    infos ={
       "COD. BANCO":"NUM_PROPOSTA",
       "DATA PG. CORRETOR":"DAT_CREDITO",
       "VALOR LIQUIDO":"VAL_BASE_COMISSAO",
       "COMISSAO":"VAL_COMISSAO",
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    df_novo = pd.DataFrame(columns=cols_opcoes.COL_OPCOES)

    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]


    df_novo["NUM_BANCO"] = 8768
    df_novo["NOM_BANCO"] = "PHTECH"
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo