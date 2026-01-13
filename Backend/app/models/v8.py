import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

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

def v8(df):
        
    df = pd.read_excel(df)

    infos ={
        "NUM_PROPOSTA":"NUM_PROPOSTA",
        "DAT_CREDITO":"DAT_CREDITO",
        "VAL_BASE_COMISSAO":"VAL_BASE_COMISSAO",
        "VAL_COMISSAO_TOTAL":"VAL_COMISSAO",
        "PERCENTUAL_REPASSE_TOTAL":"PCL_COMISSAO",
        "NUM_CONTRATO": "NUM_CONTRATO",
        "COD_PRODUTO" : "COD_PRODUTO",
        "DSC_PRODUTO" : "DSC_PRODUTO"
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    if"NUM_PROPOSTA"in df.columns:
        df["NUM_PROPOSTA"] = df["NUM_PROPOSTA"].astype(str)



    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    df_novo = pd.DataFrame(columns=col_opcoes)

    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["NUM_BANCO"] = '1725'
    df_novo["NOM_BANCO"] = 'V8 DIGITAL'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'

    return df_novo