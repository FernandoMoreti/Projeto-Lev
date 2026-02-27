from abc import ABC, abstractmethod
import pandas as pd
import os
import requests
from ..utils import getAuthToken
import json
import io
from ..banks.factory import banks

class Bank(ABC):

    def __init__(self, name: str, num: int, type: str):
        self._name = name
        self._num = num
        self._type = type

    @abstractmethod
    def readArchive(self):
        pass

    def getReportByQueueId(queueId):

        token = getAuthToken()

        header = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "insomnia/12.2.0"
        }

        try:

            response = requests.get(
                f'https://beta.uploader.elegen.com.br/api/v1/queues/{queueId}/file',
                headers=header,
            )

            responseData = response.json()

            bytesArray = responseData["data"]["file"]["data"]
            binary = bytes(bytesArray)

            archiveInMemory = io.BytesIO(binary)

            df = pd.read_excel(archiveInMemory)

            return df

        except:
            print("Algo deu errado")

    def inputProposalInEvent(df, queueId, bank):

        token = getAuthToken()

        header = {
            "Authorization": token,
            "Content-Type": "application/json",
            "User-Agent": "insomnia/12.2.0"
        }

        mapper = banks.get(bank)

        for line in df.itertuples():

            payload = mapper.map(line)

            body = {
                "queueId": queueId,
                "resourceType": "COMMISSION_RECEIVED",
                "resourceId": 1,
                "action": "CREATE",
                "payload": payload
            }

            try:
                requests.post("https://beta.uploader.elegen.com.br/api/v1/events/operations/", json=body, headers=header)
            except:
                print("Erro inesperado ao subir proposta")

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