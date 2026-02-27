from abc import ABC, abstractmethod
import pandas as pd
import os
import requests
from ..utils import getAuthToken
import io
from ..robot.factory import factoryBanksMapper

class Bank(ABC):

    def __init__(self, name: str, num: int, type: str):
        self._name = name
        self._num = num
        self._type = type

    @abstractmethod
    def readArchive(self):
        pass

    def getReportByQueueId(self, queueId):

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

    def inputProposalsInEvent(self, df, queueId, bank):

        token = getAuthToken()

        header = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "insomnia/12.2.0"
        }

        mapper = factoryBanksMapper.get(bank)

        print("Inicializando o upload proposta por proposta")

        listNotInEvents = []
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
                    timeout=15
                )
                if not response.ok:
                    listNotInEvents.append(line.get("Número Proposta"))
            except:
                listNotInEvents.append(line.get("Número Proposta"))
        session.close()
        if len(listNotInEvents) > 0:
            print(f"Propostas subiram com sucesso, exceto: {listNotInEvents}")
        else:
            print("Propostas subiram com sucesso")

    def inputAllProposalInListByQueue(self, queueId: int):
        from ..utils import getAllProposalByQueueId

        return getAllProposalByQueueId(queueId)

    def joinProposalsInDataframe(self, proposals: list):
        df = pd.DataFrame(proposals)

        return df

    def validDataframe(self, df, infos):
        from ..utils import validDf
        return validDf(df, infos)

    def createDataframe(self):
        from ..utils import createDataframe
        df_novo = createDataframe()
        return df_novo

    def inputValues(self, df, df_novo, infos):
        from ..utils import inputValueColumns
        df_novo = inputValueColumns(df, df_novo, infos)
        return df_novo

    @abstractmethod
    def run(self, df):
        pass