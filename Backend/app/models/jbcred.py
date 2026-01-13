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

def jbcred(df):

    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")

    df = pd.read_html(df, header=0)[0]

    infos ={
        "NRCONTRATO":"NUM_PROPOSTA",
        "VLR_OPER":"VAL_BASE_COMISSAO",
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

    num_propostas = []

    for num in df_novo["NUM_PROPOSTA"]:
        num_str = str(num)
        num_str = num_str.replace("-", "")
        num_str = float(num_str)
        num_propostas.append(num_str)
        
    df_novo["NUM_PROPOSTA"] = num_propostas
    df_novo["DAT_CREDITO"] = current_date
    df_novo["NOM_BANCO"] = "JBCRED"
    df_novo["PCL_COMISSAO"] = 10
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] / 10
    df_novo["NUM_BANCO"] = 777
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo