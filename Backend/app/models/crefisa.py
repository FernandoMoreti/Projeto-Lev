import pandas as pd
from datetime import datetime, timedelta
from ..utils import createDataframe, inputValueColumns, validDf

def crefisa_adiantamento(df):

    df = pd.read_excel(df, engine="xlrd")

    infos ={
       "Num_Proposta":"NUM_PROPOSTA",
       "Data_Geracao_Comissao":"DAT_CREDITO",
       "Vlr_Liquido":"VAL_BASE_COMISSAO",
       "Vlr_Pagamento_Comissao":"VAL_COMISSAO",
       "Perc_Pagamento_Comissao":"PCL_COMISSAO",
       "Tipo":"TIPO_COMISSAO_BANCO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

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