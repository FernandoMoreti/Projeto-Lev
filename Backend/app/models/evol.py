import pandas as pd

col_opcoes = [
   "NUM_BANCO",
   "NOM_BANCO",
   "NUM_PROPOSTA",
   "NUM_CONTRATO",
   "NOM_CLIENTE",
   "COD_CPF_CLIENTE",
   "DSC_PRODUTO",
   "DSC_SITUACAO_BANCO",
   "DSC_OBSERVACAO",
   "DAT_CREDITO",
   "VAL_BRUTO",
   "VAL_LIQUIDO",
   "VAL_SALDO_REFINANCIAMENTO",
   "VAL_BASE_COMISSAO",
   "VAL_COMISSAO",
   "PCL_COMISSAO",
   "DSC_TIPO_COMISSAO",
   "COD_LOJA",
   "COD_UNIDADE_EMPRESA",
   "COD_BANCO",
   "COD_TIPO_PROPOSTA_EMPRESTIMO",
   "DSC_TIPO_PROPOSTA_EMPRESTIMO",
   "NIC_CTR_USUARIO",
   "COD_PRODUTO",
   "COD_PRODUTOR_VENDA",
   "COD_PRODUTOR_VENDA_BANCO",
   "COD_TIPO_COMISSAO",
   "COD_SITUACAO_EMPRESTIMO",
   "QTD_PARCELA",
   "NUM_PARCELA_DIFERIDA_EMPRESA",
   "DAT_EMPRESTIMO",
   "DAT_CONFIRMACAO",
   "DAT_ESTORNO",
   "DAT_CTR_INCLUSAO",
   "TIPO_COMISSAO_BANCO",
   "PCL_TAXA_EMPRESTIMO"
]

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
    
    df_novo = pd.DataFrame(columns=col_opcoes)

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