import pandas as pd


def qualibank(df, cols_opcoes):
        
    df = pd.read_excel(df)

    infos ={
       "NUMERO_CTT":"NUM_PROPOSTA",
       "DATA_PAGAMENTO":"DAT_CREDITO",
       "VALOR_BASE":"VAL_BASE_COMISSAO",
       "VALOR_INCENTIVO":"VAL_COMISSAO",
       "PERC_INCENTIVO":"PCL_COMISSAO",
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

    df_novo["NUM_BANCO"] = 2222222
    df_novo["NOM_BANCO"] = "QUALI BANK"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo