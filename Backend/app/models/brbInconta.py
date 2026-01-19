import pandas as pd
import camelot
from ..utils import createDataframe, inputValueColumns, validDf

def brbInconta(df):

    tables = camelot.read_pdf(df, pages='all',flavor="stream")

    if not tables:
        return "Nenhuma tabela encontrada no PDF"

    isBigger = False

    for index, table in enumerate(tables):
        if index == 1:
            if len(table.df.columns) > 5:
                table.df = table.df.drop(columns=[1])
                table.df = table.df.drop(columns=[2])
                table.df = table.df.drop(columns=[5])
                table.df.columns = range(table.df.shape[1])
        if len(table.df[0]) > 45:
            table.df = table.df.drop(columns=[1])
            table.df.columns = range(table.df.shape[1])
            isBigger = True
        else:
            if isBigger or index == 1:
                table.df = table.df.iloc[2:]
            else:
                table.df = table.df.iloc[6:]

    df = pd.concat([table.df for table in tables], ignore_index=True)

    df = df.replace(r'^\s*$', pd.NA, regex=True)

    df = df.dropna(thresh=8) # remove linhas que tenham pelo menos 10 colunas preenchidas

    if len(df.columns) > 8:
        df = df.drop(columns=[1])
        df.columns = range(df.shape[1])

    df[4] = df[4].replace(pd.NA, 0)

    return df

    infos = {
        1 : "NUM_PROPOSTA",
        2 : "DSC_OBSERVACAO",
        3 : "QTD_PARCELA",
        4 : "PCL_COMISSAO",
        6 : "VAL_BASE_COMISSAO",
        7 : "VAL_COMISSAO",
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

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
    df_novo["NUM_PROPOSTA"] = df_novo["NUM_PROPOSTA"].astype(int)
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["NUM_BANCO"] = 70
    df_novo["NOM_BANCO"] = 'BRB - BANCO DE BRASÍLIA'
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["DSC_OBSERVACAO"] = None

    return df_novo