import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta

def crefisa_adiantamento(df, cols_opcoes):
        
    df = pd.read_excel(df, engine="xlrd")

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
    df_novo = pd.DataFrame(columns=cols_opcoes)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["NUM_BANCO"] = '69'
    df_novo["NOM_BANCO"] = 'BANCO CREFISA S.A.'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    if"TIPO_COMISSAO_BANCO"in df_novo.columns:
        df_novo.loc[df_novo["TIPO_COMISSAO_BANCO"] == "à vista","TIPO_COMISSAO_BANCO"] ="DIRETA"
       
           # Gerar o caminho do arquivo
    data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
    caminho_arquivo = f'Z:\COMISSÃO\PROJETO TESTE\CREFISA\CREFISA_{data_arquivo}.xlsx'

    # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)
    

    return caminho_arquivo