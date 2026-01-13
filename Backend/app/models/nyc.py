import pandas as pd

def nyc(df, cols_opcoes):

    df = pd.read_excel(df)
    df = df.iloc[:-3]

    infos ={
       "Id":"NUM_PROPOSTA",
       "Data Base":"DAT_CREDITO",
       "ValorLiquido":"VAL_BASE_COMISSAO",
       "Valor Comissão":"VAL_COMISSAO",
       "% Comissão":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '1728'
    df_novo["NOM_BANCO"] = 'NYC BANK'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    return df_novo