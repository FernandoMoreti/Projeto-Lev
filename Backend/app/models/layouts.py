import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import openpyxl
import json
import os

#LAYOUT WORKBANK
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
    infos ={
       "Nr Proposta":"NUM_PROPOSTA",
       "Data Integração":"DAT_CREDITO",
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=col_opcoes)



    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["NUM_BANCO"] = '7996'
    df_novo["NOM_BANCO"] = 'AMIGOZ'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    def expandir_linhas(row_original, row_mapeada):
        novas_linhas = []

        if row_original.get("Seguro") =="Diamante":
            # valor_calculado = row_original["Valor NOTA FISCAL"] - ((row_original["% Comissao"] + row_original["% Seguro"]) * row_original["Valor Liberado Cliente"]) - row_original["Comissao por Emissão"]
            # if valor_calculado not in [0,"-", None]:
            nova_linha = row_mapeada.copy()
            nova_linha["TIPO_COMISSAO_BANCO"] ="SEGURO DIAMANTE"
            nova_linha["VAL_COMISSAO"] = row_original["Valor Seguro"]
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Liberado Cliente"]
            novas_linhas.append(nova_linha)
        # Verificar condições no DataFrame original
        elif row_original.get("Valor Seguro", 0) not in [0,"-", None]:
            nova_linha = row_mapeada.copy()
            nova_linha["TIPO_COMISSAO_BANCO"] ="SEGURO"
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Liberado Cliente"]
            nova_linha["VAL_COMISSAO"] = row_original["Valor Seguro"]
            novas_linhas.append(nova_linha)

        if row_original.get("Comissao por Emissão", 0) not in [0,"-", None]:
            nova_linha = row_mapeada.copy()
            nova_linha["TIPO_COMISSAO_BANCO"] ="PRE-ADESÃO"
            nova_linha["VAL_COMISSAO"] = row_original["Comissao por Emissão"]
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Comissao por Emissão"]
            novas_linhas.append(nova_linha)

        if row_original.get("% Comissao", 0) not in [0,"-", None]:
            nova_linha = row_mapeada.copy()
            nova_linha["TIPO_COMISSAO_BANCO"] ="DIRETA"
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Liberado Cliente"]
            nova_linha["VAL_COMISSAO"] = row_original["Valor Liberado Cliente"] * row_original["% Comissao"]
            novas_linhas.append(nova_linha)

        return novas_linhas

    # Aplicar a expansão de linhas
    linhas_expandidas = []
    for index, row_original in df.iterrows():
        row_mapeada = df_novo.loc[index].to_dict() if index < len(df_novo) else {}
        linhas_expandidas.append(row_mapeada)
        linhas_expandidas.extend(expandir_linhas(row_original, row_mapeada))

    df_novo = pd.DataFrame(linhas_expandidas)

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    if"DAT_CREDITO"in df_novo.columns:
        df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], origin='1899-12-30', unit='D')
        df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%d/%m/%Y')

    df_novo = df_novo[df_novo["TIPO_COMISSAO_BANCO"].notna()]

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/AMIGOZ/AMIGOZ - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def ayude(df):
    print(df.columns.tolist())
    infos ={
       "ID DA PROPOSTA":"NUM_PROPOSTA",
       "CRIADO EM":"DAT_CREDITO",
       "VALOR DA PROPOSTA":"VAL_BASE_COMISSAO",
       "VALOR DA COMISSÃO":"VAL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '1723'
    df_novo["NOM_BANCO"] = 'AYUDE'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    # df_novo["PCL_COMISSAO"] = df_novo["VAL_COMISSAO"]/df_novo["VAL_BASE_COMISSAO"]

    # if"PCL_COMISSAO"in df_novo.columns:
    #     df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/AYUDE/AYUDE - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_acertoCard(df):

    infos ={
       "Adesão":"NUM_PROPOSTA",
       "Valor Calculado":"VAL_COMISSAO",
       "CALCULO DE 100%":"VAL_BASE_COMISSAO",
       "Com(%)":"PCL_COMISSAO",
       "Data do Acerto":"DAT_CREDITO",
       "Motivo do Acerto":"DSC_TIPO_COMISSAO"
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["TIPO_COMISSAO_BANCO"] = 'ESTORNO DE ANTECIPAÇÃO'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_ACERTOCARD {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_acertos(df):

    infos ={
       "Adesão":"NUM_PROPOSTA",
       "Valor Bruto de Comissão":"VAL_COMISSAO",
       "CALCULO DE 100%":"VAL_BASE_COMISSAO",
       "Com(%)":"PCL_COMISSAO",
       "Data do Acerto":"DAT_CREDITO",
       "Motivo do Acerto":"DSC_TIPO_COMISSAO"
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["TIPO_COMISSAO_BANCO"] = 'ESTORNO DE ANTECIPAÇÃO'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_ACERTOS {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_cartaoBenef(df):

    infos ={
       "Número da ADE":"NUM_PROPOSTA",
       "Vlr. Bruto":"VAL_COMISSAO",
       "Vlr. Base":"VAL_BASE_COMISSAO",
       "Perc. %":"PCL_COMISSAO",
       "Data Agendamento":"DAT_CREDITO",
       "Observação":"DSC_TIPO_COMISSAO",
       "Tipo de Comissionamento":"TIPO_COMISSAO_BANCO",
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_CARTAOBENEFICIO {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_cartaoBenefDif(df):

    infos ={
       "Número da ADE":"NUM_PROPOSTA",
       "Vlr. Bruto":"VAL_COMISSAO",
       "Vlr. Base":"VAL_BASE_COMISSAO",
       "Perc. %":"PCL_COMISSAO",
       "Data Agendamento":"DAT_CREDITO",
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIFERIDO'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_CARTAOBENEFICIO_DIF {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_consig(df):

    infos ={
       "Número da ADE":"NUM_PROPOSTA",
       "Vlr. Bruto":"VAL_COMISSAO",
       "Vlr. Base":"VAL_BASE_COMISSAO",
       "Perc. %":"PCL_COMISSAO",
       "Data Agendamento":"DAT_CREDITO",
       "Observação":"DSC_TIPO_COMISSAO",
        # TIPO_COMISSAO_BANCO: Recebemos DIRETA e ESTORNO nesse relatório
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_CONSIG {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_seguro(df):

    infos ={
       "Nro. da Adesão":"NUM_PROPOSTA",
       "Vlr. Bruto":"VAL_COMISSAO",
       "Vlr. Base":"VAL_BASE_COMISSAO",
       "Perc. %":"PCL_COMISSAO",
       "Dt. Agendamento":"DAT_CREDITO",
       "Observação":"DSC_TIPO_COMISSAO"
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = 'SEGURO/ESTORNO DE SEGURO'

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_SEGURO {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_reposicaoCard(df):

    infos ={
       "Adesão":"NUM_PROPOSTA",
       "Valor Bruto":"VAL_COMISSAO",
       "CALCULO DE 100%":"VAL_BASE_COMISSAO",
       "Data do Agendamento":"DAT_CREDITO"
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["PCL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = 'ESTORNO DIFERIDO'

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_REPOSICAO_CARD {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_saldoPago(df):

    infos ={
       "Adesão":"NUM_PROPOSTA",
       "Valor Bruto":"VAL_COMISSAO",
       "Valor Base":"VAL_BASE_COMISSAO",
       "Data de Pagamento":"DAT_CREDITO",
       "% Valor Presente":"PCL_COMISSAO",
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = 'ANTECIPAÇÃO'

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_SALDO_PAGO {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_saldoPagoCardBenef(df):

    infos ={
       "Adesão":"NUM_PROPOSTA",
       "Valor Presente":"VAL_COMISSAO",
       "Valor Base":"VAL_BASE_COMISSAO",
       "Data de Pagamento":"DAT_CREDITO",
       "% Valor Presente":"PCL_COMISSAO",
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = 'ANTECIPAÇÃO'

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_SALDOPADO_CARDBENEF {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_saque(df):

    infos ={
       "Nro. da Adesao":"NUM_PROPOSTA",
       "Vlr. Bruto":"VAL_COMISSAO",
       "Vlr. Base":"VAL_BASE_COMISSAO",
       "Dt. Agendamento":"DAT_CREDITO",
       "Perc. %":"PCL_COMISSAO",
       "Observacao":"DSC_TIPO_COMISSAO",
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_SAQUE {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bmg_saqueDif(df):

    infos ={
       "Número da ADE":"NUM_PROPOSTA",
       "Vlr. Bruto":"VAL_COMISSAO",
       "Vlr. Base":"VAL_BASE_COMISSAO",
       "Dt. Agendamento":"DAT_CREDITO",
       "Perc. %":"PCL_COMISSAO",
       "Observacao":"DSC_TIPO_COMISSAO",
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

    df_novo["NUM_BANCO"] = '318'
    df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIFERIDO'

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BMG/BMG_SAQUE_DIFERIDO {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def brbInconta(df):

    infos ={
       "Proposta":"NUM_PROPOSTA",
       "Vlr Venda":"VAL_COMISSAO",
       "Com(%)":"PCL_COMISSAO",
       "Data Pagamento":"DAT_CREDITO"
        #FALTA APLICAR DAT CREDITO (Vem mescalada com o nome do agente e a data do pagamento)
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

    df_novo["NUM_BANCO"] = '70'
    df_novo["NOM_BANCO"] = 'BRB INCONTA'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BRB/BRB/BRB_INCONTA_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def brb360(df):

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "CONTRATO":"NUM_CONTRATO",
       "VAL. REPASSE":"VAL_BASE_COMISSAO",
       "VAL. COMISSÃO":"VAL_COMISSAO",
       "% CMS":"PCL_COMISSAO",
       "BAIXA CMS":"DAT_CREDITO",
       "TIPO CMS":"TIPO_COMISSAO_BANCO"
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

    df_novo["NUM_BANCO"] = '701'
    df_novo["NOM_BANCO"] = 'BRB360'
    # df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BRB/BRB TEDDY - 360/BRB_360_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def bv(df):

    infos ={
       "NUM_PROPOSTA":"NUM_PROPOSTA",
       "NUM_CONTRATO":"NUM_CONTRATO",
       "DAT_PAGAMENTO":"DAT_CREDITO",
       "VAL_LIQUIDO":"VAL_BASE_COMISSAO",
       "VAL_COMISSAO":"VAL_COMISSAO"
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    print('colunas_origem_presentes', colunas_origem_presentes)
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=col_opcoes)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["NUM_BANCO"] = '44'
    df_novo["NOM_BANCO"] = 'BV'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["DAT_CREDITO"] = datetime.now().strftime('%d/%m/%Y')

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/BV/BV - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def caixa(df):

    infos ={
       "Nr Proposta":"NUM_PROPOSTA",
       "Valor Liberado Cliente":"VAL_BASE_COMISSAO",
       "Valor Líquido Pago":"VAL_COMISSAO",
       "% Comissao":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '104'
    df_novo["NOM_BANCO"] = 'CAIXA'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["DAT_CREDITO"] = datetime.now().strftime('%d/%m/%Y')

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/CBA -CAIXA/CAIXA_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def crefaz(df):

    infos ={
       "OPERAÇÃO":"NUM_PROPOSTA",
       "DT Pagamento":"DAT_CREDITO",
       "Vlr. Operação":"VAL_BASE_COMISSAO",
       "R$ Comissão":"VAL_COMISSAO",
       "%Comissão":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '1964'
    df_novo["NOM_BANCO"] = 'CREFAZ'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/CREFAZ/CREFAZ_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def crefisa_adiantamento(df):

    infos ={
       "Num_Proposta":"NUM_PROPOSTA",
       "Data_Geracao_Comissao":"DAT_CREDITO",
       "Vlr_Liquido":"VAL_BASE_COMISSAO",
       "Vlr_Pagamento_Comissao":"VAL_COMISSAO",
       "Perc_Pagamento_Comissao":"PCL_COMISSAO",
       "Tipo":"TIPO_COMISSAO_BANCO"
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

    df_novo["NUM_BANCO"] = '69'
    df_novo["NOM_BANCO"] = 'CREFISA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"TIPO_COMISSAO_BANCO"in df_novo.columns:
        df_novo.loc[df_novo["TIPO_COMISSAO_BANCO"] =="à vista","TIPO_COMISSAO_BANCO"] ="DIRETA"

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/CREFISA/CREFISA_ADIANT_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def c6auto(df):

    infos ={
       "Contrato":"NUM_PROPOSTA",
       "Dt. Produção Date":"DAT_CREDITO",
       "Vlr. Principal Base":"VAL_BASE_COMISSAO",
       "Vlr. Líquido":"VAL_COMISSAO",
       "% de Comissão Total":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '3336'
    df_novo["NOM_BANCO"] = 'C6 AUTO'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/C6 AUTO/C6AUTO_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def c6avista(df):

    infos ={
       "Número Proposta":"NUM_PROPOSTA",
       "Data Pagamento":"DAT_CREDITO",
       "Vlr Base":"VAL_BASE_COMISSAO",
       "Vlr Bruto":"VAL_COMISSAO",
       "Perc à Vista":"PCL_COMISSAO",
       "Tipo De Comissao":"TIPO_COMISSAO_BANCO",
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

    df_novo["NUM_BANCO"] = '336'
    df_novo["NOM_BANCO"] = 'C6 BANK'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # Aplicar regra da comissão zerada se a loja não for 'LEV'
    if"Loja Recebedora"in df.columns:
        df_novo["VAL_COMISSAO"] = df.apply(
            lambda row: 0 if row["Loja Recebedora"] !="LEV"else row.get("Vlr Bruto", 0),
            axis=1
        )

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/C6 BANK/C6AVISTA_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def digio(df):

    infos ={
       "PROP.":"NUM_PROPOSTA",
       "Dt. Pgto Cmss.":"DAT_CREDITO",
       "Base de Cálculo":"VAL_BASE_COMISSAO",
       "Valor Comiss":"VAL_COMISSAO",
       "Parâm":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '335'
    df_novo["NOM_BANCO"] = 'DIGIO'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # if"PCL_COMISSAO"in df_novo.columns:
    #     df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/DIGIO/DIGIO {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def dryve(df):

    infos ={
       "Reference Code":"NUM_PROPOSTA",
       "Valor da Venda":"VAL_BASE_COMISSAO",
       "Valor de Comissão 2Qn":"VAL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '1110'
    df_novo["NOM_BANCO"] = 'DRYVE'
    df_novo["DAT_CREDITO"] = datetime.now().strftime("%d/%m/%Y")
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/DRYVE/DRYVE - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def euro17(df):

    infos ={
       "NuOperacao":"NUM_PROPOSTA",
       "horario_pgto":"DAT_CREDITO",
       "VlContrato":"VAL_BASE_COMISSAO",
       "VlComissao":"VAL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '359108'
    df_novo["NOM_BANCO"] = 'EURO17'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"DAT_CREDITO"in df_novo.columns:
        df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], origin='1899-12-30', unit='D')
        df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%d/%m/%Y')

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/EURO 17/EURO17 - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def futuro(df):

    infos ={
       "Operação":"NUM_PROPOSTA",
       "Data Geração da Comissão":"DAT_CREDITO",
       "Valor Nominal":"VAL_BASE_COMISSAO",
       "Valor Comissão Corban":"VAL_COMISSAO",
       "Percentual Comissão Corban":"PCL_COMISSAO"
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


    df_novo["NUM_BANCO"] = '8888'
    df_novo["NOM_BANCO"] = 'FUTURO PREVIDENCIA'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/FUTUROPREV/FUTUROPREV - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def grandino(df):

    infos ={
       "Nro Proposta":"NUM_PROPOSTA",
       "Data de Fechamento":"DAT_CREDITO",
       "Base de C\u00e1lculo":"VAL_BASE_COMISSAO",
       "Valor Comiss\u00e3o":"VAL_COMISSAO",
       "Porcentagem":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '88888'
    df_novo["NOM_BANCO"] = 'GRANDINO LTDA'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/GRANDINO/GRANDINO - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def happy(df):

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "CONTRATO":"NUM_CONTRATO",
       "BAIXA CMS":"DAT_CREDITO",
       "VAL. REPASSE":"VAL_BASE_COMISSAO",
       "VAL. COMISSÃO":"VAL_COMISSAO",
       "% CMS":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '1010'
    df_novo["NOM_BANCO"] = 'HAPPY CONSIGNADO'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/HAPPY - TEDDY/HAPPY - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def icred(df):

    infos ={
       "Number":"NUM_PROPOSTA",
       "commission_report_reference_date":"DAT_CREDITO",
       "commission_base":"VAL_BASE_COMISSAO",
       "commission_value":"VAL_COMISSAO",
       "commission_factor":"PCL_COMISSAO",
       "commission_type":"TIPO_COMISSAO_BANCO"
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

    df_novo["NUM_BANCO"] = '329'
    df_novo["NOM_BANCO"] = 'ICRED'
    df_novo["TIPO_COMISSAO_BANCO"] = df_novo["TIPO_COMISSAO_BANCO"].replace('Flat', 'DIRETA')
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # Ajustar valores de % Comissão
    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    if"DAT_CREDITO"in df_novo.columns:
        df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], origin='1899-12-30', unit='D')
        df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%d/%m/%Y')

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/ICRED/ICRED_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def inbursa(df):

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "CONTRATO":"NUM_CONTRATO",
       "BAIXA CMS":"DAT_CREDITO",
       "VAL. REPASSE":"VAL_BASE_COMISSAO",
       "VAL. COMISSÃO":"VAL_COMISSAO",
       "% CMS":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '12'
    df_novo["NOM_BANCO"] = 'INBURSA'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'

    df_novo["DAT_CREDITO"] = pd.to_numeric(df_novo["DAT_CREDITO"], errors='coerce')
    df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], origin='1899-12-30', unit='D')
    df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%d/%m/%Y')

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100


    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/INBURSA - TEDDY/INBURSA - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def jbcred(df):

    infos ={
       "NR_PROPOSTA":"NUM_PROPOSTA",
       "DT_ULT_REC":"DAT_CREDITO",
       "VLR_LIQ":"VAL_BASE_COMISSAO",
       "VL_COMISSAO":"PCL_COMISSAO"
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

    # Ajuste para pegar apenas os 12 primeiros dígitos da proposta
    if"NUM_PROPOSTA"in df_novo.columns:
        df_novo["NUM_PROPOSTA"] = df_novo["NUM_PROPOSTA"].astype(str).str[:12]
        
    df_novo["NUM_BANCO"] = '777'
    df_novo["NOM_BANCO"] = 'JBCRED'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/JBCRED/JBCRED_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def kardbank(df):

    infos ={
       "Número Ade":"NUM_PROPOSTA",
       "Data Pgto Cliente":"DAT_CREDITO",
       "Valor Base do Contrato":"VAL_BASE_COMISSAO",
       "Valor":"VAL_COMISSAO",
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

    df_novo["NUM_BANCO"] = '6910'
    df_novo["NOM_BANCO"] = 'KARDBANK'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/KARDBANK/KARDBANK - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def master_antecipacao(df):

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "DATA_FECHAMENTO":"DAT_CREDITO",
       "VLR_FINANC":"VAL_BASE_COMISSAO",
       "COMISSÃO LIQUIDA":"VAL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '243'
    df_novo["NOM_BANCO"] = 'MASTER'
    df_novo["TIPO_COMISSAO_BANCO"] = 'ANTECIPAÇÃO'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # if"PCL_COMISSAO"in df_novo.columns:
    #     df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/MASTER/MASTER_ANTECIP {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def master_flat(df):

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "DATA_FECHAMENTO":"DAT_CREDITO",
       "VLR_FINANC":"VAL_BASE_COMISSAO",
       "Vlr. Bruto":"VAL_COMISSAO",
       "VLR_COM":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '243'
    df_novo["NOM_BANCO"] = 'MASTER'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # if"PCL_COMISSAO"in df_novo.columns:
    #     df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/MASTER/MASTER_FLAT {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def mercantil(df):
    print(df.columns.tolist())
    infos ={
       "CONTRATO":"NUM_PROPOSTA",
       "TARIFA CORRESPONDENTE":"VAL_BASE_COMISSAO",
       "TARIFA CORRES":"VAL_BASE_COMISSAO",
       "VALOR CORRESP":"VAL_BASE_COMISSAO",
       "VALOR SUBST":"VAL_BASE_COMISSAO"
    }
    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    # Criar o novo DataFrame com todas as colunas necessárias
    df_novo = pd.DataFrame(columns=col_opcoes)
    
    # Mapear as colunas disponíveis
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns and col_destino in col_opcoes:
            df_novo[col_destino] = df[col_origem]
    
    # Verificar colunas essenciais
    colunas_essenciais = ["NUM_PROPOSTA","VAL_BASE_COMISSAO"]
    if not all(col in df_novo.columns for col in colunas_essenciais):
        return"ErroColunas"

    df_novo["NUM_BANCO"] = '389'
    df_novo["NOM_BANCO"] = 'MERCANTIL'
    df_novo["DAT_CREDITO"] = datetime.now().strftime("%d/%m/%Y")
    df_novo["TIPO_COMISSAO_BANCO"] = 'PRÉ ADESAO'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"]

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/MERCANTIL/Comissão/MERCANTIL_PRE_ADESÃO_WORK {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def meucash(df):

    infos ={
       "Nro Proposta":"NUM_PROPOSTA",
       "Data Movimentação":"DAT_CREDITO",
       "Valor Liberado":"VAL_BASE_COMISSAO",
       "Comissão_R$":"VAL_COMISSAO",
       "Comissão_%":"PCL_COMISSAO"
    }
    
    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    df = df[df["Nro Proposta"].notna()]
    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=col_opcoes)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["NUM_BANCO"] = '666'
    df_novo["NOM_BANCO"] = 'MEUCASHCARD'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100


    if"DAT_CREDITO"in df_novo.columns:
        df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], origin='1899-12-30', unit='D')
        df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%d/%m/%Y')

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/MEUCASHCARD/CASHCARD_WL_CASAQUI_SERV_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def novo_saque(df):

    infos ={
       "N de Contrato":"NUM_PROPOSTA",
       "Pgto. Comissão":"DAT_CREDITO",
       "R$ Liberado":"VAL_BASE_COMISSAO",
       "R$ Corban":"VAL_COMISSAO",
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

    df_novo["NUM_BANCO"] = '1234'
    df_novo["NOM_BANCO"] = 'NOVO SAQUE'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # if"PCL_COMISSAO"in df_novo.columns:
    #     df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/NOVO SAQUE/NOVO_SAQUE_ {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def nyc(df):
    print(df.columns.tolist())
    infos ={
       "Id":"NUM_PROPOSTA",
       "Data pagamento comissão":"DAT_CREDITO",
       "ValorLiquido":"VAL_BASE_COMISSAO",
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

    df_novo["NUM_BANCO"] = '1728'
    df_novo["NOM_BANCO"] = 'NYC BANK'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

    if"DAT_CREDITO"in df_novo.columns:
        df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], origin='1899-12-30', unit='d')
        df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%d/%m/%Y')

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/NYC/NYC_RelatorioComissoes_ {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def oleFVE(df):

    infos ={
       "Proposta":"NUM_PROPOSTA",
       "Valor Líquido":"VAL_BASE_COMISSAO",
       "Valor A Vista":"VAL_COMISSAO",
       "Percentual Comissão":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '218'
    df_novo["NOM_BANCO"] = 'BANCO OLE'
    df_novo["DAT_CREDITO"] = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 1

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/SANTANDER FVE/OLE_FVE {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def phtech(df):

        infos ={
           "COD. BANCO":"NUM_PROPOSTA",
           "DATA PG. CORRETOR":"DAT_CREDITO",
           "VALOR LIQUIDO":"VAL_BASE_COMISSAO",
           "COMISSAO":"VAL_COMISSAO"
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

        #df_novo["NUM_BANCO"] = '8770'
        df_novo["NUM_BANCO"] = '8768'
        df_novo["NOM_BANCO"] = 'PHTECH'
        df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
        df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
        df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"].astype(float) / df_novo["VAL_BASE_COMISSAO"].astype(float)) * 100

        # Gerar o caminho do arquivo
        data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
        caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/PH/PHTECH - {data_arquivo}.xlsx'

        # Salvar como Excel
        df_novo.to_excel(caminho_arquivo, index=False)

        return caminho_arquivo

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
    
def sabemi(df):

    infos ={
       "Proposta":"NUM_PROPOSTA",
       "Data Liberacao":"DAT_CREDITO",
       "Comissão":"VAL_COMISSAO",
       "Percentual Comissão":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '5'
    df_novo["NOM_BANCO"] = 'SABEMI'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"Valor AF Bruto"in df.columns and"Valor Af Liquido"in df.columns and"Operação"in df.columns:
        df_novo["VAL_BASE_COMISSAO"] = df.apply(
            lambda row: row["Valor Af Liquido"] if row["Operação"] =="SFGTS"else row["Valor AF Bruto"], axis=1
        )
    else:""

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/SABEMI/SABEMI - {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo    

def safra(df):

        infos ={
           "Contrato":"NUM_PROPOSTA",
           "Nome Cliente":"NOM_CLIENTE",
           "CPF":"COD_CPF_CLIENTE",
           "Nome Tabela Juros":"DSC_PRODUTO",
           "Comissionado SRCC":"DSC_SITUACAO_BANCO",
           "Data efetivacao Contrato":"DAT_CREDITO",
           "Valor Principal":"VAL_BRUTO",
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

    #     df_novo["VAL_BRUTO"] = df_novo["VAL_BRUTO"].apply(
    #     lambda x: f"{x * 1000:.2f}".replace(".",",") if isinstance(x, float) and '.' in str(x) else f"{x:.2f}".replace(".",",")
    # )

        df_novo["NUM_BANCO"] = '42'
        df_novo["NOM_BANCO"] = 'SAFRA'
        df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
        df_novo["DSC_OBSERVACAO"] = df_novo["DSC_SITUACAO_BANCO"]
        df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BRUTO"]
        df_novo["TIPO_COMISSAO_BANCO"] = 'AUTORREGULAÇAO'
        df_novo["COD_CPF_CLIENTE"] = df_novo["COD_CPF_CLIENTE"].astype(str).apply(lambda cpf: cpf.zfill(11))

        data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
        caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/SAFRA/COMISSÕES ZERO/SAFRA_{data_arquivo}.xlsx'

        df_novo.to_excel(caminho_arquivo, index=False)

        return caminho_arquivo

def safra_novo(df):

        infos ={
           "Contrato":"NUM_PROPOSTA",
           "Nome Cliente":"NOM_CLIENTE",
           "CPF":"COD_CPF_CLIENTE",
           "Nome Tabela Juros":"DSC_PRODUTO",
            #"Comissionado SRCC":"DSC_SITUACAO_BANCO",
           "Data efetivacao":"DAT_CREDITO",
           "Valor Base Comissao":"VAL_BRUTO",
           "Vl Pagamento Bruto Comissao":"VAL_COMISSAO",
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

    #     df_novo["VAL_BRUTO"] = df_novo["VAL_BRUTO"].apply(
    #     lambda x: f"{x * 1000:.2f}".replace(".",",") if isinstance(x, float) and '.' in str(x) else f"{x:.2f}".replace(".",",")
    # )

        df_novo["NUM_BANCO"] = '42'
        df_novo["NOM_BANCO"] = 'SAFRA'
        df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
        df_novo["DSC_OBSERVACAO"] = df_novo["DSC_SITUACAO_BANCO"]
        df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BRUTO"]
        df_novo["TIPO_COMISSAO_BANCO"] = 'AUTORREGULAÇAO'
        df_novo["COD_CPF_CLIENTE"] = df_novo["COD_CPF_CLIENTE"].astype(str).apply(lambda cpf: cpf.zfill(11))

        data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
        caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/SAFRA/COMISSÕES ZERO/SAFRA_{data_arquivo}.xlsx'

        df_novo.to_excel(caminho_arquivo, index=False)

        return caminho_arquivo

def santanderFVE(df):
    print(df.columns.tolist())
    infos ={
       "Proposta":"NUM_PROPOSTA",
       "Valor Líquido":"VAL_BASE_COMISSAO",
       "Valor A Vista":"VAL_COMISSAO",
       "Percentual Comissão":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '351'
    df_novo["NOM_BANCO"] = 'SANTANDER'
    df_novo["DAT_CREDITO"] = (datetime.now() - timedelta(days=1)).strftime("%d/%m/%Y")
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 1

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/SANTANDER FVE/FVE VI {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def totalcash(df):

    infos ={
       "Nr Proposta":"NUM_PROPOSTA",
       "Valor Liberado Cliente":"VAL_BASE_COMISSAO",
       "Valor Comissão":"VAL_COMISSAO",
       "% Comissao":"PCL_COMISSAO",
       "Data Status":"DAT_CREDITO"
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

    df_novo["NUM_BANCO"] = '1731'
    df_novo["NOM_BANCO"] = 'TOTALCASH'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"PCL_COMISSAO"in df_novo.columns:
        df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 1

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/TOTAL CASH/TOTALCASH_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def vctex(df):
    infos = {
       "Número do Contrato":"NUM_PROPOSTA",
       "N�mero do Contrato":"NUM_PROPOSTA",
       "Data de Repasse Comissão":"DAT_CREDITO",
       "Data de Repasse Comiss�o":"DAT_CREDITO",
       "Valor Liberado":"VAL_BASE_COMISSAO",
       "Valor Comissão":"VAL_COMISSAO",
       "Valor Comiss�o":"VAL_COMISSAO",
       "% Comissão":"PCL_COMISSAO",
       "% Comiss�o":"PCL_COMISSAO"
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    # Criar o novo DataFrame com todas as colunas necessárias
    df_novo = pd.DataFrame(columns=col_opcoes)
    
    # Mapear as colunas disponíveis
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns and col_destino in col_opcoes:
            df_novo[col_destino] = df[col_origem]
    
    # Verificar colunas essenciais
    colunas_essenciais = ["NUM_PROPOSTA","DAT_CREDITO","VAL_BASE_COMISSAO","VAL_COMISSAO"]
    if not all(col in df_novo.columns for col in colunas_essenciais):
        return"ErroColunas"

    # Preencher colunas fixas
    df_novo["NUM_BANCO"] = '1530'
    df_novo["NOM_BANCO"] = 'VCTEX CORRESPONDENTE'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    
    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/VCTEX/VCTEX - relatorio_comissao {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def vemcard(df):

        infos ={
           "Número CCB":"NUM_PROPOSTA",
           "Data de Pagamento":"DAT_CREDITO",
           "Vlr Liquido do Cliente":"VAL_BASE_COMISSAO",
           "Valor da Comissão":"VAL_COMISSAO",
           "Taxa da Comissão":"PCL_COMISSAO"
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

        df_novo["NUM_BANCO"] = '1727'
        df_novo["NOM_BANCO"] = 'VEMCARD'
        df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
        df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

        if"PCL_COMISSAO"in df_novo.columns:
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

        # Gerar o caminho do arquivo
        data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
        caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/VEMCARD/VEMCARD_CONSIG {data_arquivo}.xlsx'

        # Salvar como Excel
        df_novo.to_excel(caminho_arquivo, index=False)

        return caminho_arquivo

def vemcardFGTS(df):

    infos ={
       "Nro Proposta":"NUM_PROPOSTA",
       "Data de Integração":"DAT_CREDITO",
       "Valor Líquido":"VAL_BASE_COMISSAO",
       "Comissão":"VAL_COMISSAO",
       "Percentual Comissão":"PCL_COMISSAO"
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

    df_novo["NUM_BANCO"] = '1727'
    df_novo["NOM_BANCO"] = 'VEMCARD'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/VEMCARD/VEMCARD_FGTS {data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def v8digital(df):

        infos ={
           "NUM_PROPOSTA":"NUM_PROPOSTA",
           "DAT_CREDITO":"DAT_CREDITO",
           "VAL_BASE_COMISSAO":"VAL_BASE_COMISSAO",
           "VAL_COMISSAO_TOTAL":"VAL_COMISSAO",
           "PERCENTUAL_REPASSE_TOTAL":"PCL_COMISSAO"
        }
        if not isinstance(df, pd.DataFrame):
            return"Erro: A entrada não é um DataFrame válido."

        if"NUM_PROPOSTA"in df.columns:
            df["NUM_PROPOSTA"] = df["NUM_PROPOSTA"].astype(str)



        colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
        if not colunas_origem_presentes:
            return"ErroColunas"

        # Criar o DataFrame com as colunas desejadas
        df_novo = pd.DataFrame(columns=col_opcoes)

        # Mapeamento de colunas
        for col_origem, col_destino in infos.items():
            if col_origem in df.columns:
                df_novo[col_destino] = df[col_origem]

        df_novo["NUM_BANCO"] = '1725'
        df_novo["NOM_BANCO"] = 'V8 DIGITAL'
        df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
        df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

        if"DAT_CREDITO"in df_novo.columns:
            df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], origin='1899-12-30', unit='D')
            df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%d/%m/%Y')


        data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
        caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/V8/V8 - {data_arquivo}.xlsx'

        df_novo.to_excel(caminho_arquivo, index=False)

        return caminho_arquivo

def work(df):
    infos = {
       "PROPOSTA":"NUM_PROPOSTA",
       "CONTRATO":"NUM_CONTRATO",
       "À PAGAR":"DAT_CREDITO",
       "VALOR BASE":"VAL_BASE_COMISSAO",
       "VALOR CMS BANCO":"VAL_COMISSAO",
       "% CMS":"PCL_COMISSAO",
       "TIPO CMS BANCO":"TIPO_COMISSAO_BANCO",
       "STATUS":"DSC_OBSERVACAO"
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar novo DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=col_opcoes)

    for col_origem, col_destino in infos.items():
        df_novo[col_destino] = df[col_origem]

    # Manter apenas linhas onde DSC_OBSERVACAO é"SEM PROPOSTA"
    df_novo = df_novo[df_novo["DSC_OBSERVACAO"] =="SEM PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = df_novo["TIPO_COMISSAO_BANCO"].str.split("-").str[-1]

    df_novo["NUM_BANCO"] = 'COLOCAR MANUAL'
    df_novo["NOM_BANCO"] = 'COLOCAR MANUAL'
    df_novo["DSC_OBSERVACAO"] = ''
    if"DAT_CREDITO"in df_novo.columns:
        df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], origin='1899-12-30', unit='D')
        df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%d/%m/%Y')

    # Salvar em Excel
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/WORK-RETROATIVO/RETROATIVO - {data_arquivo}.xlsx'

    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

#EDIÇÕES
def c6bank(df):
    newColumns = ["Cliente","CPF/CNPJ","Cidade Servidor","Data Oper/ Data Inclusão","Data Pagamento","Gerente","Número Proposta","Tipo de Operação","Vlr Base","Vlr Bruto","Irrf","Iss","Inss","Vlr Liquido","Perc à Vista","Tac","Parcelas","Taxa Contrato","Situação","Observacao","Contrato Digitador Por","Loja Origem","UF Loja Origem","Cod Produto","Produto","Código Agente","Código Tabela","Data Ini Vig","Data Fim Vig","Vlr Financiado","Oper Original","Saldo Devedor","Pmt Original","Vlr Pmt Original","Perc Pmt Liquidado","Fator","Vlr Pmt Nova","Perc Valor Ajustado","Forma Liquidação","Contrato Complementar","Pmt Contr Compl","Perc Red Consig","Perc Red Calc Spread","Data Agendamento","Percentual Sobre Índice","Número Cartão","Mat Cliente","Nro Parcela","Sistema Origem","Data Registro","Tipo De Comissao","Banco Origem Recompra","CPF do Agente","Data de Vencimento","Previsão Comissão Parcelada","Percentual Manutenção","Tabela Cod Desc","Cod Comissionado","Nome Comissionado","Débito SRCC","Modalidade Negócio","Cod Master Imediato","Nome Master Imediato","Nome Digitador","Agência Cliente","Banco Cliente","Conta Cliente","Perc De Comissao","CodBeneficio","Desc Beneficio","Categoria Comissão","Data Formalização","TaxaCL","Detalhe Pagamento","Possui Seguro?","Possui TC?"]

    infos = {
   "Cliente":"Cliente",
   "CPF/CNPJ":"CPF/CNPJ",
   "Cidade Servidor":"Cidade Servidor",
   "Data Oper/ Data Inclusão":"Data Oper/ Data Inclusão",
   "Data Pagamento":"Data Pagamento",
   "Gerente":"Gerente",
   "Número Proposta":"Número Proposta",
   "Tipo de Operação":"Tipo de Operação",
   "Vlr Base":"Vlr Base",
   "Vlr Bruto":"Vlr Bruto",
   "Irrf":"Irrf",
   "Iss":"Iss",
   "Inss":"Inss",
   "Vlr Liquido":"Vlr Liquido",
   "Perc à Vista":"Perc à Vista",
   "Tac":"Tac",
   "Parcelas":"Parcelas",
   "Taxa Contrato":"Taxa Contrato",
   "Situação":"Situação",
   "Observacao":"Observacao",
   "Contrato Digitador Por":"Contrato Digitador Por",
   "Loja Origem":"Loja Origem",
   "UF Loja Origem":"UF Loja Origem",
   "Cod Produto":"Cod Produto",
   "Produto":"Produto",
   "Código Agente":"Código Agente",
   "Código Tabela":"Código Tabela",
   "Data Ini Vig":"Data Ini Vig",
   "Data Fim Vig":"Data Fim Vig",
   "Vlr Financiado":"Vlr Financiado",
   "Oper Original":"Oper Original",
   "Saldo Devedor":"Saldo Devedor",
   "Pmt Original":"Pmt Original",
   "Vlr Pmt Original":"Vlr Pmt Original",
   "Perc Pmt Liquidado":"Perc Pmt Liquidado",
   "Fator":"Fator",
   "Vlr Pmt Nova":"Vlr Pmt Nova",
   "Perc Valor Ajustado":"Perc Valor Ajustado",
   "Forma Liquidação":"Forma Liquidação",
   "Contrato Complementar":"Contrato Complementar",
   "Pmt Contr Compl":"Pmt Contr Compl",
   "Perc Red Consig":"Perc Red Consig",
   "Perc Red Calc Spread":"Perc Red Calc Spread",
   "Data Agendamento":"Data Agendamento",
   "Percentual Sobre Índice":"Percentual Sobre Índice",
   "Número Cartão":"Número Cartão",
   "Mat Cliente":"Mat Cliente",
   "Nro Parcela":"Nro Parcela",
   "Sistema Origem":"Sistema Origem",
   "Data Registro":"Data Registro",
   "Tipo De Comissao":"Tipo De Comissao",
   "Banco Origem Recompra":"Banco Origem Recompra",
   "CPF do Agente":"CPF do Agente",
   "Data de Vencimento":"Data de Vencimento",
   "Previsão Comissão Parcelada":"Previsão Comissão Parcelada",
   "Percentual Manutenção":"Percentual Manutenção",
   "Tabela Cod Desc":"Tabela Cod Desc",
   "Cod Comissionado":"Cod Comissionado",
   "Nome Comissionado":"Nome Comissionado",
   "Débito SRCC":"Débito SRCC",
   "Modalidade Negócio":"Modalidade Negócio",
   "Cod Master Imediato":"Cod Master Imediato",
   "Nome Master Imediato":"Nome Master Imediato",
   "Nome Digitador":"Nome Digitador",
   "Agência Cliente":"Agência Cliente",
   "Banco Cliente":"Banco Cliente",
   "Conta Cliente":"Conta Cliente",
   "Perc De Comissao":"Perc De Comissao",
   "CodBeneficio":"CodBeneficio",
   "Desc Beneficio":"Desc Beneficio",
   "Categoria Comissão":"Categoria Comissão",
   "Data Formalização":"Data Formalização",
   "TaxaCL":"TaxaCL",
   "Detalhe Pagamento":"Detalhe Pagamento",
   "Possui Seguro?":"Possui Seguro?",
   "Possui TC?":"Possui TC?"
    }


    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=newColumns)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    if"Nome Comissionado"in df.columns:
        df_novo["Vlr Bruto"] = df_novo.apply(lambda row: 0 if row["Nome Comissionado"] !="LEV"else row["Vlr Bruto"], axis=1)

    if"Nome Digitador"in df_novo.columns:
        df_novo["Nome Digitador"] = df_novo["Nome Digitador"].str.strip()

    colunas_data = ["Data Oper/ Data Inclusão","Data Pagamento","Data Ini Vig","Data Fim Vig","Data Agendamento","Data Registro","Data de Vencimento","Data Formalização"]
    for coluna in colunas_data:
        if coluna in df_novo.columns:
            df_novo[coluna] = pd.to_datetime(df_novo[coluna], errors='coerce', unit='D', origin='1899-12-30')
            df_novo[coluna] = df_novo[coluna].dt.strftime('%d/%m/%Y')

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d.%m")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/C6 BANK/COMISSÃO/Analítico Comissão à Vista- {data_arquivo} - editado.xlsx'

    # Salvar como EXCEL
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def c6kgiro(df):
    newColumns = ["Cod Loja","Cod Convênio","Nome Convênio","Proposta Consignado","Valor Contrato Consignado","Taxa Contrato Consignado","Cod Produto","Produto","Cod Tabela","Tabela","Usuário Digitador","Elegível Kgiro","Observação","Data Digitação","Data Produção","Contrato Kgiro","Valor Total Kgiro","Taxa Kgiro","Prazo Kgiro","Data Pagamento Kgiro","Data Vencimento Primeira Parcela Kgiro","Banco","Valor Kgiro","Valor Liberado Consignado","Valor Estimado Antecipação","Perc Estimado Antecipação","Valor Diferido Total","% Comissão VF","Nome Corban","Tipo Antecipação Detalhe","Tipo Antecipação"]

    infos = {
   "Cod Loja":"Cod Loja",
   "Cod Convênio":"Cod Convênio",
   "Nome Convênio":"Nome Convênio",
   "Proposta Consignado":"Proposta Consignado",
   "Valor Contrato Consignado":"Valor Contrato Consignado",
   "Taxa Contrato Consignado":"Taxa Contrato Consignado",
   "Cod Produto":"Cod Produto",
   "Produto":"Produto",
   "Cod Tabela":"Cod Tabela",
   "Tabela":"Tabela",
   "Usuário Digitador":"Usuário Digitador",
   "Elegível Kgiro":"Elegível Kgiro",
   "Observação":"Observação",
   "Data Digitação":"Data Digitação",
   "Data Produção":"Data Produção",
   "Contrato Kgiro":"Contrato Kgiro",
   "Valor Total Kgiro":"Valor Total Kgiro",
   "Taxa Kgiro":"Taxa Kgiro",
   "Prazo Kgiro":"Prazo Kgiro",
   "Data Pagamento Kgiro":"Data Pagamento Kgiro",
   "Data Vencimento Primeira Parcela Kgiro":"Data Vencimento Primeira Parcela Kgiro",
   "Banco":"Banco",
   "Valor Kgiro":"Valor Kgiro",
   "Valor Liberado Consignado":"Valor Liberado Consignado",
   "Valor Estimado Antecipação":"Valor Estimado Antecipação",
   "Perc Estimado Antecipação":"Perc Estimado Antecipação",
   "Valor Diferido Total":"Valor Diferido Total",
   "% Comissão VF":"% Comissão VF",
   "Nome Corban":"Nome Corban",
   "Tipo Antecipação Detalhe":"Tipo Antecipação Detalhe",
   "Tipo Antecipação":"Tipo Antecipação"
    }


    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=newColumns)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    colunas_data = ["Data Digitação","Data Produção","Data Pagamento Kgiro","Data Vencimento Primeira Parcela Kgiro"]
    for coluna in colunas_data:
        if coluna in df_novo.columns:
            df_novo[coluna] = pd.to_datetime(df_novo[coluna], errors='coerce', unit='D', origin='1899-12-30')
            df_novo[coluna] = df_novo[coluna].dt.strftime('%d/%m/%Y')

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d.%m")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/C6 BANK/KGIRO/Analítico Kgiro - Emitidos {data_arquivo}.xlsx'

    # Salvar como EXCEL
    df_novo.to_excel(caminho_arquivo, index=False)

    try:
        os.remove(f'Z:/COMISSÃO/DOCS - WORK BANK 2025/C6 BANK/KGIRO/Analítico Kgiro - Emitidos.xlsx')
    except OSError as e:
        return f"Erro ao excluir a base original: {e}"

    return caminho_arquivo

def facta_92359(df):
    newColumns = [   "CODIGOAF","NUMERO_CONTRATO","CORRETOR","TIPOCONTACORRETOR","DATA","DEBITO","CREDITO","OBSERVACAO","VLRAF","NR_COMISS","NM_COMISS","EMPRESA","DATA_DIGITACAO","TABELA","SALDO","COR"]

    infos = {
   "CODIGOAF":"CODIGOAF",
   "NUMERO_CONTRATO":"NUMERO_CONTRATO",
   "CORRETOR":"CORRETOR",
   "TIPOCONTACORRETOR":"TIPOCONTACORRETOR",
   "DATA":"DATA",
   "DEBITO":"DEBITO",
   "CREDITO":"CREDITO",
   "OBSERVACAO":"OBSERVACAO",
   "VLRAF":"VLRAF",
   "NR_COMISS":"NR_COMISS",
   "NM_COMISS":"NM_COMISS",
   "EMPRESA":"EMPRESA",
   "DATA_DIGITACAO":"DATA_DIGITACAO",
   "TABELA":"TABELA",
   "SALDO":"SALDO",
   "COR":"COR"
    }


    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=newColumns)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    # colunas_data = ["DATA","DATA_DIGITACAO"]
    # for coluna in colunas_data:
    #     if coluna in df_novo.columns:
    #         df_novo[coluna] = pd.to_datetime(df_novo[coluna], errors='coerce', unit='D', origin='1899-12-30')
    #         df_novo[coluna] = df_novo[coluna].dt.strftime('%d/%m/%Y')

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d.%m")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/FACTA/EXTRATO CMS PERIODO/Relatorio Conta Corrente {data_arquivo}_92359 - editado.xlsx'

    # Salvar como EXCEL
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo

def facta_94569(df):
    newColumns = [   "CODIGOAF","NUMERO_CONTRATO","CORRETOR","TIPOCONTACORRETOR","DATA","DEBITO","CREDITO","OBSERVACAO","VLRAF","NR_COMISS","NM_COMISS","EMPRESA","DATA_DIGITACAO","TABELA","SALDO","COR"]

    infos = {
   "CODIGOAF":"CODIGOAF",
   "NUMERO_CONTRATO":"NUMERO_CONTRATO",
   "CORRETOR":"CORRETOR",
   "TIPOCONTACORRETOR":"TIPOCONTACORRETOR",
   "DATA":"DATA",
   "DEBITO":"DEBITO",
   "CREDITO":"CREDITO",
   "OBSERVACAO":"OBSERVACAO",
   "VLRAF":"VLRAF",
   "NR_COMISS":"NR_COMISS",
   "NM_COMISS":"NM_COMISS",
   "EMPRESA":"EMPRESA",
   "DATA_DIGITACAO":"DATA_DIGITACAO",
   "TABELA":"TABELA",
   "SALDO":"SALDO",
   "COR":"COR"
    }


    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=newColumns)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    # colunas_data = ["DATA","DATA_DIGITACAO"]
    # for coluna in colunas_data:
    #     if coluna in df_novo.columns:
    #         df_novo[coluna] = pd.to_datetime(df_novo[coluna], errors='coerce', unit='D', origin='1899-12-30')
    #         df_novo[coluna] = df_novo[coluna].dt.strftime('%d/%m/%Y')

    # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d.%m")
    caminho_arquivo = f'Z:/COMISSÃO/DOCS - WORK BANK 2025/FACTA/EXTRATO CMS PERIODO/Relatorio Conta Corrente {data_arquivo}_94569 - editado.xlsx'

    # Salvar como EXCEL
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo