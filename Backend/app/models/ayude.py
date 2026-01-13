import pandas as pd

def ayude(df, cols_opcoes):

    df_soli = pd.read_excel(df, sheet_name="DADOS DA SOLICITAÇÃO", )
    df = pd.read_excel(df, sheet_name="PROPOSTAS PRÓPRIAS", )
    df = df.iloc[:-3]

    infos ={
       "ID DA PROPOSTA":"NUM_PROPOSTA",
       "VALOR DA PROPOSTA":"VAL_BASE_COMISSAO",
       "VALOR DA COMISSÃO":"VAL_COMISSAO"
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=cols_opcoes)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["NUM_BANCO"] = '1723'
    df_novo["NOM_BANCO"] = 'AYUDE'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["DAT_CREDITO"] = df_soli["SOLICITADO EM"]
    df_novo["PCL_COMISSAO"] = df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"] * 100

    return df_novo