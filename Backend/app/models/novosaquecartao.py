import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def novosaquecartao(df):
    df = pd.read_csv(df, sep=";")

    infos = {
        "N de Contrato": "NUM_PROPOSTA",
        "Valor Bruto": "VAL_BASE_COMISSAO",
        "Comissão Total": "VAL_COMISSAO",
        "Pgto. Comissão": "DAT_CREDITO",
        "% Comissão Total": "PCL_COMISSAO"
    }

    Error = validDf(df, infos)
    if Error:
        return Error

    df_novo = createDataframe()

    df_novo = inputValueColumns(df, df_novo, infos)

    valores_tratados = []

    for valor in df_novo["VAL_BASE_COMISSAO"]:

        valor_str = valor

        if type(valor) == str:

            valor_str = str(valor)
            valor_teste = valor_str.replace("R$", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_teste = valor_teste.strip()
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_BASE_COMISSAO"] = valores_tratados

    valores_tratados = []

    for valor in df_novo["VAL_COMISSAO"]:

        valor_str = valor

        if type(valor) == str:

            valor_str = str(valor)
            valor_teste = valor_str.replace("R$", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_teste = valor_teste.strip()
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["VAL_COMISSAO"] = valores_tratados

    valores_tratados = []

    for valor in df_novo["PCL_COMISSAO"]:

        valor_str = valor

        if type(valor) == str:

            valor_str = str(valor)
            valor_teste = valor_str.replace("%", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_teste = valor_teste.strip()
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df_novo["PCL_COMISSAO"] = valores_tratados

    df_novo["NUM_BANCO"] = 1234
    df_novo["NOM_BANCO"] = "NOVO SAQUE"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo
