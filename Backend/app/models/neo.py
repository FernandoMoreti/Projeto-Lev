import pandas as pd
from datetime import datetime

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

def neo(df):

    data = df.filename.split("_")[1].split(".")[0]
    resultado = f"{data[:2]}/{data[2:4]}/{data[4:]}"

    df = pd.read_excel(df)

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "VALOR BRUTO":"VAL_BASE_COMISSAO",
       "CMS R$":"VAL_COMISSAO",
       "CMS %":"PCL_COMISSAO",       
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"
    
    df_novo = pd.DataFrame(columns=col_opcoes)

    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    tamanho = len(df_novo)

    df_novo = df_novo.drop(index=[tamanho -1, tamanho -2, tamanho -3, tamanho -4])

    df_novo["PCL_COMISSAO"] = round(df_novo["PCL_COMISSAO"] * 100, 2)

    df_novo["NUM_BANCO"] = 3333333
    df_novo["NOM_BANCO"] = "NEO CREDITO"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["DAT_CREDITO"] = resultado

    return df_novo