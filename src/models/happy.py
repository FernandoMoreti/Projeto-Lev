import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import openpyxl
import json
import os


caminho_arquivo = r"Z:\COMISSÃO\TIME\Nandão\EXTRATORES_COMISSÃO\src\assets\Acerto da Producao 01.09.xlsx"
nome_data = os.path.splitext(os.path.basename(caminho_arquivo))[0].replace(".", "-").split()[3]

df_test = pd.read_excel(r"Z:\COMISSÃO\TIME\Nandão\Projeto\Projeto Lev\src\assets\Acerto da Producao 01.09.xlsx", header=2 )


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

def happy(df):

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "DT PAGTO":"DAT_CREDITO",
       "VR BASE":"VAL_BASE_COMISSAO",
       "VR CMS":"VAL_COMISSAO",
       "% CMS":"PCL_COMISSAO",
       
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."
    
    tamanho = len(df["PROPOSTA"])
    
    df = df.drop(index=[tamanho -1])


    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=col_opcoes)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str)
    mascara = df_novo["VAL_BASE_COMISSAO"].str.len() <= 6
    df_novo.loc[mascara, "VAL_BASE_COMISSAO"] = df_novo.loc[mascara, "VAL_BASE_COMISSAO"].str.replace(".", ",", regex=False)
    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].str.replace(".", "").str.replace(",", ".").astype(float)
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["NUM_BANCO"] = 1010
    df_novo["NOM_BANCO"] = 'HAPPY CONSIGNADO'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # Gerar o caminho do arquivo
    caminho_arquivo = f'Z:/COMISSÃO/TIME/Nandão/HAPPY/ HAPPY - {nome_data}.xlsx'

    # # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

print(happy(df_test))
