import pandas as pd
from datetime import datetime, timedelta

def queromais(df, cols_opcoes):

    df = pd.read_excel(df)

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
    df_novo = pd.DataFrame(columns=cols_opcoes)

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

         
    # Gerar o caminho do arquivo
    data_arquivo = (datetime.now() - timedelta(days=1)).strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:/COMISSÃO/PROJETO TESTE/QUERO+/QUERO+_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo