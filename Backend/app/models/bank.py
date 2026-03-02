from abc import ABC, abstractmethod
import pandas as pd

class Bank(ABC):

    def __init__(self, name: str, num: int, type: str):
        self._name = name
        self._num = num
        self._type = type

    @abstractmethod
    def readArchive(self):
        pass

    def getReportByQueueId(self, queueId):
        from ..utils import getReportByqueueId

        return getReportByqueueId(queueId)

    def inputProposalsInEvent(self, df, queueId, bank):
        from ..utils import inputProposalInEvent

        inputProposalInEvent(df, queueId, bank)

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