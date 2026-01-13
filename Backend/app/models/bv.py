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

def bv(df):

    data = datetime.now().strftime("%d/%m/%Y")

    df = pd.read_excel(df)

    infos ={
       "NUM_PROPOSTA":"NUM_PROPOSTA",
       "NUM_CONTRATO":"NUM_CONTRATO",
       "VAL_LIQUIDO": "VAL_BASE_COMISSAO",
       "VAL_COMISSAO":"VAL_COMISSAO"
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=col_opcoes)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    valores_tratados = []

    for valor in df_novo["VAL_BASE_COMISSAO"]:    
        
        valor_str = valor

        if type(valor) == str:

            valor_str = str(valor)
            valor_teste = valor_str.replace("R$", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_teste = valor_teste.strip()
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_BASE_COMISSAO"] = valores_tratados
    
    valores_tratados = []


    for valor in df_novo["VAL_COMISSAO"]:    
        
        valor_str = valor

        if type(valor) == str:

            valor_str = str(valor)
            valor_teste = valor_str.replace("R$", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_teste = valor_teste.strip()
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_COMISSAO"] = valores_tratados
    df_novo["DAT_CREDITO"] = data
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"] * 100)
    df_novo["NUM_BANCO"] = 44
    df_novo["NOM_BANCO"] = 'BV'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    return df_novo