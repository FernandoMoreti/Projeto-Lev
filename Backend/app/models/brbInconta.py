import pandas as pd
import camelot
from ..utils import createDataframe, inputValueColumns, validDf

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

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

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