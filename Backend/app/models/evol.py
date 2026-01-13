import pandas as pd
import cols_opcoes

def evol(df):
    
    df = pd.read_excel(df)

    infos ={
        "Id_Operation":"NUM_PROPOSTA",
        "Taxa":"PCL_TAXA_EMPRESTIMO",
        "Valor_Liberado":"VAL_LIQUIDO",
        "Comissão":"VAL_COMISSAO",  
        "Valor_Bruto":"VAL_BRUTO",  
        "Data Finalizacao":"DAT_CREDITO",
        "Percentual_Comissao":"PCL_COMISSAO",
        "Descricao_Tipo_Operacao" :"DSC_TIPO_PROPOSTA_EMPRESTIMO"   
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

    for index, row in df_novo.iterrows():
        if row["DSC_TIPO_PROPOSTA_EMPRESTIMO"] == "PORT + REFIN - NORMAL":
            df_novo.at[index, "VAL_BASE_COMISSAO"] = row["VAL_LIQUIDO"]
        else:
            df_novo.at[index, "VAL_BASE_COMISSAO"] = row["VAL_BRUTO"]

    df_novo["NOM_BANCO"] = "EVOL"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["NUM_BANCO"] = 7777
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["DSC_TIPO_PROPOSTA_EMPRESTIMO"] = None
    
    return df_novo