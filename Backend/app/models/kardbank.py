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

def kardbank(df):

    df = pd.read_html(df, header=0)[0]

    df.to_excel("teste_kardbank.xlsx")

    infos ={
        "Número Ade":"NUM_PROPOSTA",
        "Data Pgto Vendedor":"DAT_CREDITO",
        "Valor Bruto":"VAL_BASE_COMISSAO",
        "% Comissão":"PCL_COMISSAO",       
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

    valores_tratados = []

    for valor in df_novo["VAL_BASE_COMISSAO"]:    
        
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)
            valor_teste = valor_str.replace("R$ ", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)
    
    df_novo["VAL_BASE_COMISSAO"] = valores_tratados

    df_novo["NOM_BANCO"] = "KARDBANK"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] * (df_novo["PCL_COMISSAO"] / 100)
    df_novo["NUM_BANCO"] = 6910
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo