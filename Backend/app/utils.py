import os
import smtplib
from email.message import EmailMessage
import pandas as pd
import requests
import json
import io
from .robot.factory import factoryBanksMapper
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
    print("Toke de autenticação obtido com sucesso")

    return token

def getReportByqueueId(queueId):
    token = getAuthToken()

    header = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "insomnia/12.2.0"
    }

    try:
        print("Buscando o arquivo")

        response = requests.get(
            f'{os.environ.get("URL_UPLOADER_GET_ARCHIVE")}{queueId}/file',
            headers=header,
        )

        responseData = response.json()

        bytesArray = responseData["data"]["file"]["data"]
        binary = bytes(bytesArray)

        archiveInMemory = io.BytesIO(binary)

        df = pd.read_excel(archiveInMemory)

        print("Arquivo encontrado e lido com sucesso")

        return df
    except:
        print(f"Erro ao buscar relaotrio do id: {queueId}")

def inputProposalInEvent(df, queueId, bank):
    token = getAuthToken()

    header = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "insomnia/12.2.0"
    }

    mapper = factoryBanksMapper.get(bank)

    print("Inicializando o upload proposta por proposta")

    listNotInEvents = []
    proposalTotal = 0
    session = requests.Session()
    session.headers.update(header)

    for line in df.to_dict(orient="records"):

        payload = mapper.map(line)

        body = {
            "queueId": queueId,
            "resourceType": "COMMISSION_RECEIVED",
            "resourceId": 1,
            "action": "CREATE",
            "payload": payload
        }

        try:
            response = session.post(
                os.environ.get("URL_UPLOADER_POST_PROPOSAL"),
                json=body,
            )
            if not response.ok:
                listNotInEvents.append(line.get("Número Proposta"))
            else:
                proposalTotal += 1
        except:
            listNotInEvents.append(line.get("Número Proposta"))

    session.close()
    if len(listNotInEvents) > 0:
        print(f"Propostas subiram com sucesso, exceto: {len(listNotInEvents)} --> {listNotInEvents}")
        print(f"Total de propsotas: {proposalTotal}")
    else:
        print("Propostas subiram com sucesso")
        print(f"Total de propsotas: {proposalTotal}")

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

def sendMail(bank, fileName, attachments=None):
    email = os.getenv("SENDMAIL_LOGIN_EMAIL")
    password = os.getenv("SENDMAIL_LOGIN_PASSWORD")
    recipient = "comissao@levnegocios.com.br"

    msg = EmailMessage()
    msg['Subject'] = f"Relatorio de comissao do banco: {bank}"
    msg['From'] = email
    msg['To'] = recipient
    msg.set_content("Relatorio de comissao do banco, pronto para processar")
    msg.add_attachment(
        attachments,
        maintype='application',
        subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        filename=fileName
    )

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email, password)
            smtp.send_message(msg)
            print("E-mail enviado com sucesso!")
    except Exception as e:
        print(f"Erro ao enviar: {e}")

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

        try:
            v = str(valor).replace("R$", "").strip()
            if "," in v and "." in v:
                v = v.replace(".", "").replace(",", ".")
            elif "," in v:
                v = v.replace(",", ".")

            if "-" in v:
                v = v.replace("-", "").strip()
                v = "-" + v

            valor_str = float(v)

            valores_tratados.append(valor_str)
        except (ValueError, TypeError):
            valores_tratados.append(0.0)

    return valores_tratados

def paintLine(row):
    if row["NUM_PROPOSTA"] == 0:
        return ["background-color: #ffcccc"] * len(row)
    return [""] * len(row)

def createListByLine(df):
    listOfProposal = []

    for index, row in df.iterrows():

        if pd.isna(row["NUM_PROPOSTA"]) or pd.isna(row["VAL_COMISSAO"]):
            continue

        data = {
            "bank": row["NOM_BANCO"],
            "proposal": row["NUM_PROPOSTA"],
            "date": row["DAT_CREDITO"],
            "valBase": round(row["VAL_BASE_COMISSAO"], 2),
            "valCommission": round(row["VAL_COMISSAO"], 2),
            "pclCommission": round(row["PCL_COMISSAO"], 2),
            "typeCommission": row["TIPO_COMISSAO_BANCO"],
        }

        listOfProposal.append(data)

    return listOfProposal