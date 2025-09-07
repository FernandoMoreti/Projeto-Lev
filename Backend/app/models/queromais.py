import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import openpyxl
import json
import os

print("importações OK")

caminho_arquivo = r"Z:\COMISSÃO\TIME\Nandão\Projeto\Projeto Lev\src\assets\BV_COMISSAO_SETEMBRO 03.09.xlsx"

df_test = pd.read_excel(r"Z:\COMISSÃO\TIME\Nandão\Projeto\Projeto Lev\src\assets\BV_COMISSAO_SETEMBRO 03.09.xlsx")

nome_data = os.path.splitext(os.path.basename(caminho_arquivo))[0].replace(".", "-").split()[1]

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

def queromais(df):
    infos = {
       "NR.PROP.":"NUM_PROPOSTA",
       "Dt Pag Comissão":"DAT_CREDITO",
       "VLR TOTAL PRODUCUÇÃO (VLR LIQUIDO + SEGURO)":"VAL_BASE_COMISSAO",
       "Valor Comissão":"VAL_COMISSAO",
       "% Comissão":"PCL_COMISSAO"
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

    # Adicionar colunas fixas
    df_novo["NUM_BANCO"] = '3030'
    df_novo["NOM_BANCO"] = 'QUERO MAIS CREDITO'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # Ajustar valores de % Comissão
    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    if"DAT_CREDITO"in df_novo.columns:
        df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], origin='1899-12-30', unit='d')
        df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%d/%m/%Y')

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/QUERO + CRÉDITO/COMISSÃO/QUERO+_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo