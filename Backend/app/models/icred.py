import pandas as pd

def icred(df, cols_opcoes):

    df = pd.read_excel(df)

    infos ={
       "Number":"NUM_PROPOSTA",
       "Data":"DAT_CREDITO",
       "commission_base":"VAL_BASE_COMISSAO",
       "commission_factor": "PCL_COMISSAO",
       "commission_value":"VAL_COMISSAO",
       "commission_type":"TIPO_COMISSAO_BANCO"
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

    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["NUM_BANCO"] = '329'
    df_novo["NOM_BANCO"] = 'ICRED'
    df_novo["TIPO_COMISSAO_BANCO"] = df_novo["TIPO_COMISSAO_BANCO"].replace('Flat', 'DIRETA')
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    return df_novo