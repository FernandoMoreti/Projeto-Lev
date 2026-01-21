from abc import ABC, abstractmethod

class Bank(ABC):

    def __init__(self, name: str, num: int, type: str):
        self._name = name
        self._num = num
        self._type = type

    @abstractmethod
    def readArchive(self):
        pass

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