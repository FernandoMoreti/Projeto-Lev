import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import requests

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

def queromaiscancelados(df):

    df = pd.read_excel(df)

    infos = {
       "CONTRATO":"NUM_PROPOSTA",
       "Valor Prêmio":"VAL_COMISSAO",
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

    list_val_bruto = []

    for prop in df_novo["NUM_PROPOSTA"]:
        data = requests.get(f"http://192.168.1.252:3004/v1/wb-api/proposta/?proposal={prop}")
        if data:
            result = data.json()
            list_val_bruto.append(result[0]["bruto"])

    df_novo["VAL_BRUTO"] = list_val_bruto

    valores_tratados = []

    for valor in df_novo["VAL_BRUTO"]:    
        
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)
    
    df_novo["VAL_BRUTO"] = valores_tratados

    df_novo["NUM_BANCO"] = 3030
    df_novo["NOM_BANCO"] = 'QUERO MAIS CREDITO'
    df_novo["DAT_CREDITO"] = datetime.now().date()
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BRUTO"]
    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BRUTO"]
    df_novo["PCL_COMISSAO"] = df_novo["VAL_COMISSAO"] / df_novo["VAL_BRUTO"] * 100
    df_novo["TIPO_COMISSAO_BANCO"] = 'ESTORNO'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    return df_novo