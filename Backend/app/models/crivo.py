import pandas as pd
import logging

logger = logging.getLogger("bancos")

class Crivo():
    def __init__(self, name = "Crivo"):
        self.name = name

    def readArchive(self, df):
        try:
            df = pd.read_excel(df)
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def agroupCrivo(self, df):

        listOfCommission = []
        listOfReap = []
        listOfForm = []

        for index, row in df.iterrows():
            if row["Motivo do Crivo"] == "PENDÊNCIA TED DEVOLVIDA":
                listOfReap.append(row["Id Proposta"])
                continue
            if row["Motivo do Crivo"] == "COMISSÃO DUPLICADA":
                listOfForm.append(row["Id Proposta"])
                continue
            listOfCommission.append(row["Id Proposta"])

        return listOfCommission, listOfReap, listOfForm


    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do C6bankdebitomanual")

            df = self.readArchive(df)
            if isinstance(df, str):
                return df

            listOfCommission, listOfReap, listOfForm = self.agroupCrivo(df)

            print(f"listOfCommission: {listOfCommission}")
            print(f"listOfForm: {listOfForm}")
            print(f"listOfReap: {listOfReap}")

            logger.info("Processamento do C6bankdebitomanual finalizado com sucesso")
            return df
        except Exception:
            logger.exception("Erro ao editar C6bankdebitomanual")
            logger.error("Erro ao editar C6bankdebitomanual")
            return "Erro ao editar C6bankdebitomanual"
        finally:
            logger.info("Finalizado processo de edicao C6bankdebitomanual")