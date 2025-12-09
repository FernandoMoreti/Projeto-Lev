import pandas as pd
from datetime import datetime, date, timedelta

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

def santanderfvevi(df):

    data = date.today() - timedelta(days=1)

    df = pd.read_csv(df, sep=";")

    infos = {
        "Proposta": "NUM_PROPOSTA",
        "Valor Bruto": "VAL_BASE_COMISSAO",
        "Percentual Comissão": "PCL_COMISSAO",
        "Valor Total Comissão": "VAL_COMISSAO",
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."
    
    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    
    if not colunas_origem_presentes:
        return "Erro: O DataFrame não contém todas as colunas necessárias."
    
    df_novo = pd.DataFrame(columns=col_opcoes)
    
    for col_origem, col_destino in infos.items():
        df_novo[col_destino] = df[col_origem]

    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["NUM_BANCO"] = 351
    df_novo["NOM_BANCO"] = "SANTANDER"
    df_novo["DAT_CREDITO"] = data
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    
    return df_novo