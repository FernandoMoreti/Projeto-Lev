import pandas as pd

def vctex(df, cols_opcoes):


    df = pd.read_csv(df, sep=";")

    infos ={
       "Número do Contrato":"NUM_PROPOSTA",
       "Valor Liberado":"VAL_BASE_COMISSAO",
       "Data de Repasse Comissão": "DAT_CREDITO",
       "Valor Comissão":"VAL_COMISSAO",
       "% Comissão":"PCL_COMISSAO",       
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

    df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["NUM_BANCO"] = 1530
    df_novo["NOM_BANCO"] = "VCTEX CORRESPONDENTE"
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo