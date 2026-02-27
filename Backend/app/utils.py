import os

import pandas as pd
import requests
import json
from dotenv import load_dotenv
load_dotenv()

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

def getAuthToken():
    user = {
        "email": os.environ.get("AUTH_LOGIN_EMAIL"),
        "password": os.environ.get("AUTH_LOGIN_PASSWORD")
    }

    getToken = requests.post(
        os.environ.get("URL_GET_TOKEN_LOGIN"),
        json=user
    )

    token = f'Bearer {getToken.json()["token"]}'

    return token

def getAllProposalByQueueId(queueId: int):

    token = getAuthToken()

    header = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "insomnia/12.2.0"
    }

    listOfProposal = []
    page = 1
    isThereMorePages = True

    while isThereMorePages:

        params = {
            "page": page,
            "pageSize": 100
        }

        response = requests.get(
            f'{os.environ.get("UPLOADER_URL_GET_PROPOSAL_BY_QUEUE")}{queueId}',
            headers=header,
            params=params
        )

        response_json = response.json()

        dataByPage = response_json.get("data", [])

        if len(dataByPage) == 0:
            print("Fim das páginas alcançado!")
            isThereMorePages = False
            break

        for data in dataByPage:
            payload = json.loads(data["payload"])
            listOfProposal.append(payload)

        page += 1

    print(f"Busca finalizada! Total de propostas resgatadas: {len(listOfProposal)}")
    return listOfProposal

def createDataframe():
    newDataFrame = pd.DataFrame(columns=col_opcoes)
    return newDataFrame

def validDf(df, infos):

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())

    if not colunas_origem_presentes:
        return"ErroColunas"

def inputValueColumns(df, df_novo, infos):
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    return df_novo

def convertValues(df_novo, columns):
    valores_tratados = []

    for valor in df_novo[columns]:
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)
            valor_teste = valor_str.replace("R$", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    return valores_tratados

def paintLine(row):
    if row["NUM_PROPOSTA"] == 0:
        return ["background-color: #ffcccc"] * len(row)
    return [""] * len(row)