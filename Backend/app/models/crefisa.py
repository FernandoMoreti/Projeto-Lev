import pandas as pd
from datetime import datetime, timedelta

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