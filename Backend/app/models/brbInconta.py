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
            print("antes")
            print(t.df)
            tabela = t.df.copy()
            tabela = tabela.drop(tabela.columns[2])
            print("depois")
            print(tabela)
            t.df = tabela



    df_temp = pd.concat([t.df for t in tables], ignore_index=True)
    df_temp.to_excel("arquivo.xlsx", index=False)

    df = pd.read_excel("arquivo.xlsx", header=6)

    df = df.dropna(thresh=9) # remove linhas que tenham pelo menos 10 colunas preenchidas
    col_nome_cpf = df.columns[1]

    # separa em duas colunas
    df[["NOM_CLIENTE", "COD_CPF_CLIENTE"]] = (
        df[col_nome_cpf]
        .astype(str)
        .str.split("\n", expand=True)
    )

    # remove a coluna original (opcional)
    df = df.drop(columns=[col_nome_cpf])

    return df