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
        listOfPricing = []

        for index, row in df.iterrows():
            if row["Motivo do Crivo"] == "PENDÊNCIA TED DEVOLVIDA":
                listOfReap.append({
                    "proposta": row["Num.Proposta"]
                })
                continue
            if row["Motivo do Crivo"] == "COMISSÃO DUPLICADA":
                listOfForm.append({
                    "proposta": row["Num.Proposta"],
                    "agentId": row["Id Agente"],
                    "status": row["Situação Agente"],
                })
                continue
            if row["Motivo do Crivo"] == "PENDÊNCIA FALTA TABELA COMISSÃO":
                listOfPricing.append({
                    "proposta": row["Num.Proposta"],
                })
                continue
            listOfCommission.append({
                    "proposta": row["Num.Proposta"],
                    "motivo": row["Motivo do Crivo"]
                })

        return listOfCommission, listOfReap, listOfForm, listOfPricing


    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do C6bankdebitomanual")

            df = self.readArchive(df)
            if isinstance(df, str):
                return df

            listOfCommission, listOfReap, listOfForm, listOfPricing = self.agroupCrivo(df)

            logger.info("Processamento do C6bankdebitomanual finalizado com sucesso")
            return listOfCommission, listOfForm, listOfReap, listOfPricing
        except Exception:
            logger.exception("Erro ao editar C6bankdebitomanual")
            logger.error("Erro ao editar C6bankdebitomanual")
            return "Erro ao editar C6bankdebitomanual"
        finally:
            logger.info("Finalizado processo de edicao C6bankdebitomanual")