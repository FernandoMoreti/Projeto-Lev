import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import openpyxl
import json
import os

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

def amigoz(df):

    df = pd.read_excel(df)

    infos ={
       "Nr Proposta": "NUM_PROPOSTA",
       "Data Integração": "DAT_CREDITO",
       "Observações": "DSC_OBSERVACAO"
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

    df_novo["NUM_BANCO"] = '7996'
    df_novo["NOM_BANCO"] = 'AMIGOZ'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    def expandir_linhas(row_original, row_mapeada):
        novas_linhas = []

        # Criar linha seguro
        if row_original.get("Seguro") == "Diamante":
            nova_linha = row_mapeada.copy()
            if row_original["Valor Seguro"] < 0: 
                nova_linha["TIPO_COMISSAO_BANCO"] ="ESTORNO SEGURO"
            else:    
                nova_linha["TIPO_COMISSAO_BANCO"] ="SEGURO DIAMANTE"
            nova_linha["VAL_COMISSAO"] = row_original["Valor Seguro"]
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Proposta"]
            nova_linha["PCL_COMISSAO"] = row_original["% Seguro"]
            novas_linhas.append(nova_linha)

        # Criar linha seguro
        if row_original.get("Seguro") == "Ouro":
            nova_linha = row_mapeada.copy()
            if row_original["Valor Seguro"] < 0: 
                nova_linha["TIPO_COMISSAO_BANCO"] ="ESTORNO SEGURO"
            else:
                nova_linha["TIPO_COMISSAO_BANCO"] ="SEGURO OURO"
            nova_linha["VAL_COMISSAO"] = row_original["Valor Seguro"]
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Proposta"]
            nova_linha["PCL_COMISSAO"] = row_original["% Seguro"]
            novas_linhas.append(nova_linha)

        # Criar linha seguro
        if row_original.get("Seguro") == "Prata":
            nova_linha = row_mapeada.copy()
            if row_original["Valor Seguro"] < 0: 
                nova_linha["TIPO_COMISSAO_BANCO"] ="ESTORNO SEGURO"
            else:
                nova_linha["TIPO_COMISSAO_BANCO"] ="SEGURO PRATA"
            nova_linha["VAL_COMISSAO"] = row_original["Valor Seguro"]
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Proposta"]
            nova_linha["PCL_COMISSAO"] = row_original["% Seguro"]
            novas_linhas.append(nova_linha)

        # Criar linha Pré-Adesão
        if pd.isna(row_original.get("Comissao por Emissão", 0)) == False:
            if row_original["Comissao por Emissão"] != 0:
                nova_linha = row_mapeada.copy()
                nova_linha["TIPO_COMISSAO_BANCO"] ="PRE-ADESÃO"
                nova_linha["VAL_COMISSAO"] = row_original["Comissao por Emissão"]
                nova_linha["VAL_BASE_COMISSAO"] = row_original["Comissao por Emissão"]
                nova_linha["PCL_COMISSAO"] = 1
                novas_linhas.append(nova_linha)

        # Criar linha Comissão
        if pd.isna(row_original.get("$ Comissão")) == False:
            nova_linha = row_mapeada.copy()
            if row_original["$ Comissão"] < 0: 
                nova_linha["TIPO_COMISSAO_BANCO"] ="ESTORNO"
            else:
                nova_linha["TIPO_COMISSAO_BANCO"] ="DIRETA"
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Proposta"]
            nova_linha["VAL_COMISSAO"] = row_original["$ Comissão"]
            nova_linha["PCL_COMISSAO"] = row_original["% Comissao"]
            novas_linhas.append(nova_linha)

        return novas_linhas

    # Aplicar a expansão de linhas
    linhas_expandidas = []
    for index, row_original in df.iterrows():
        row_mapeada = df_novo.loc[index].to_dict() if index < len(df_novo) else {}
        linhas_expandidas.append(row_mapeada)
        linhas_expandidas.extend(expandir_linhas(row_original, row_mapeada))

    df_novo = pd.DataFrame(linhas_expandidas)

    if "PCL_COMISSAO" in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    if "DAT_CREDITO" in df_novo.columns:
        for i in range(len(df_novo["DAT_CREDITO"])):
            if pd.isna(df_novo["DAT_CREDITO"][i]) == True:
                df_novo["DAT_CREDITO"][i] = data_default
        df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%d/%m/%Y')

    if "DSC_OBSERVACAO" in df_novo.columns:
        mask = df_novo["DSC_OBSERVACAO"] == "Credito devido estorno feito em duplicidade"
        df_novo.loc[mask, "TIPO_COMISSAO_BANCO"] = "REEMBOLSO"

    df_novo = df_novo[df_novo["TIPO_COMISSAO_BANCO"].notna()]
    df_novo = df_novo[df_novo["VAL_COMISSAO"].notna()]

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/TIME/Nandão/AMIGOZ/ Amigoz - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo