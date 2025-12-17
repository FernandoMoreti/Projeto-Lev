import pandas as pd
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

def btw(df):

    data = f"LECCA_{df.filename.split('_')[2]}"

    caminho_pasta = "Z:\COMISSÃO\DOCS - WORK BANK 2025\BTW\\12 - DEZEMBRO"
    arquivos = os.listdir(caminho_pasta)

    arquivo_encontrado = None

    for arquivo in arquivos:
        if data in arquivo:
            arquivo_encontrado = arquivo
            break
    
    if arquivo_encontrado:
        caminho_completo = os.path.join(caminho_pasta, arquivo_encontrado)
        df_encontrado = pd.read_excel(caminho_completo)
    else:
        print("Arquivo não encontrado para a data:", data)


    df = pd.read_excel(df)

    df = pd.concat([df_encontrado, df], ignore_index=True)
    
    return df

    infos = {
        "Proposta": "NUM_PROPOSTA",
        "DT_Pagamento": "DAT_CREDITO",
        "Valor_Liberado": "VAL_BASE_COMISSAO",
        "274,31": "VAL_COMISSAO",
        "Tx_Comissao_Flat": "PCL_COMISSAO",
    }

    if not isinstance(df, pd.DataFrame):
        return "Erro: A entrada não é um DataFrame válido."
    
    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return "ErroColunas"
    
    df_novo = pd.DataFrame(columns=col_opcoes)

    for col_origem, col_destino in infos.items():
        df_novo[col_destino] = df[col_origem]
    
    df_novo["NUM_BANCO"] = 10501
    df_novo["NOM_BANCO"] = "BTW BANK"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"