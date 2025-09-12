import pandas as pd

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

def brb360(df):


    filename = df.filename
    nome_data = filename.replace(".", "-").replace("-xlsx", "").split()[3]

    df = pd.read_excel(df, header=2)

    infos ={
       "PROPOSTA": "NUM_PROPOSTA",
       "DT PAGTO": "DAT_CREDITO",
       "VR BASE": "VAL_BASE_COMISSAO",
       "VR CMS": "VAL_COMISSAO",
       "% CMS": "PCL_COMISSAO",
       "TIPO CMS": "TIPO_COMISSAO_BANCO"       
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
    df_novo["NUM_BANCO"] = 701
    df_novo["NOM_BANCO"] = 'BRB'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    # Gerar o caminho do arquivo
    caminho_arquivo = f'Z:/COMISSÃO/TIME/Nandão/BRB360/ BRB360_{nome_data} Editado.xlsx'

    # # Salvar como Excel
    df_novo.to_excel(caminho_arquivo, index=False)

    return caminho_arquivo