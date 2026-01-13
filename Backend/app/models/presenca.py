import pandas as pd
import cols_opcoes

def presenca(df):

    df = pd.read_excel(df, header=2)

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "DT PAGTO":"DAT_CREDITO",
       "VR BASE":"VAL_BASE_COMISSAO",
       "VR CMS":"VAL_COMISSAO",
       "% CMS":"PCL_COMISSAO",
       
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."
    
    tamanho = len(df["PROPOSTA"])
    
    df = df.drop(index=[tamanho -1])


    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=cols_opcoes.COL_OPCOES)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str)
    mascara = df_novo["VAL_BASE_COMISSAO"].str.len() <= 6
    df_novo.loc[mascara, "VAL_BASE_COMISSAO"] = df_novo.loc[mascara, "VAL_BASE_COMISSAO"].str.replace(".", ",", regex=False)
    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].str.replace(".", "").str.replace(",", ".").astype(float)
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["NUM_BANCO"] = 482
    df_novo["NOM_BANCO"] = 'PRESENCA BANK SCP'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    
    for i in range(len(df_novo["VAL_BASE_COMISSAO"])):
        if df_novo["VAL_BASE_COMISSAO"][i] < 0:
            df_novo.loc[i, "TIPO_COMISSAO_BANCO"] = 'ESTORNO'
        else:
            df_novo.loc[i, "TIPO_COMISSAO_BANCO"] = 'DIRETA'

    return df_novo