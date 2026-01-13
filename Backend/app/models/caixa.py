import pandas as pd
import cols_opcoes

def caixa(df):

    df = pd.read_excel(df)

    infos ={
        "Nr Proposta":"NUM_PROPOSTA",
        "Valor Liberado Cliente":"VAL_BASE_COMISSAO",
        "% Comissao":"PCL_COMISSAO",
        "Valor Nota Fiscal":"VAL_COMISSAO"      
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."
    
    
    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"Erro: Colunas necessárias não encontradas no DataFrame."
    
    df_novo = pd.DataFrame(columns=cols_opcoes.COL_OPCOES)

    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["NOM_BANCO"] = "CAIXA"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["NUM_BANCO"] = 104
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100
    return df_novo