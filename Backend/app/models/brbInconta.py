import pandas as pd
import camelot

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

def brbInconta(df):

    tables = camelot.read_pdf(df, pages='all',flavor="stream")

    if not tables:
        return "Nenhuma tabela encontrada no PDF"
    
    for index, t in enumerate(tables):
        if index == 1:
            t.df = t.df.drop(columns=[1])
            t.df = t.df.drop(columns=[2])
            t.df = t.df.dropna(axis=1, how="all")
            t.df.rename(columns={i: i-1 for i in range(1, t.df.shape[0])}, inplace=True)
        if len(t.df[0]) > 45:
            t.df = t.df.drop(columns=[1])
        else:
            t.df = t.df.iloc[6:]

    df = pd.concat([t.df for t in tables], ignore_index=True)

    df = df.replace(r'^\s*$', pd.NA, regex=True)

    df = df.dropna(thresh=8) # remove linhas que tenham pelo menos 10 colunas preenchidas

    infos = {
        2 : "NUM_PROPOSTA",
        3 : "DSC_OBSERVACAO",
        4 : "QTD_PARCELA",
        5 : "PCL_COMISSAO",
        7 : "VAL_BASE_COMISSAO",
        8 : "VAL_COMISSAO",
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

    df_novo = df_novo.iloc[:-1]

    valores_tratados = []

    for valor in df_novo["VAL_BASE_COMISSAO"]:    
        
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)
    
    df_novo["VAL_BASE_COMISSAO"] = valores_tratados
    
    valores_tratados = []

    for valor in df_novo["VAL_COMISSAO"]:    
        
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)
    
    df_novo["VAL_COMISSAO"] = valores_tratados

    valores_tratados = []

    for valor in df_novo["DSC_OBSERVACAO"]:    
        
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace("%", "")
            valor_teste = valor_teste.strip()
            valor_teste = valor_teste.split(" ")[-1]
            valor_teste = valor_teste.replace(",", ".")
            if valor_teste == "SAQUE":
                valor_teste = "0"
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)
    
    df_novo["PCL_TAXA_EMPRESTIMO"] = valores_tratados



    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["QTD_PARCELA"] = df_novo["QTD_PARCELA"].astype(int)
    df_novo["NUM_PROPOSTA"] = df_novo["NUM_PROPOSTA"].astype(int)
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["NUM_BANCO"] = 70
    df_novo["NOM_BANCO"] = 'BRB - BANCO DE BRASÍLIA'
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["DSC_OBSERVACAO"] = None

    return df_novo