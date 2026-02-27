import pandas as pd
import logging
from ...models.bank import Bank

logger = logging.getLogger("bancos")

class C6_Bank(Bank):
    def __init__(self, name = "C6 Bank", num = 3336, type = "excel"):
        super().__init__(name, num, type)

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


    def run(self, queueId, nameBank):

        try:

            print(f"Iniciando a captura do Relatorio com o id: {queueId}")
            df = self.getReportByQueueId(queueId)
            print(f"Fianlizando com sucesso, queueId: {queueId}")

            print(f"Iniciando o input da propostas no event com o QueueId: {queueId}")
            self.inputProposalsInEvent(df, queueId, nameBank)
            print(f"Finalizando o input das propostas com o QueueId: {queueId}")


            # listOfProposal = self.inputAllProposalInListByQueue(queueId)

            # df = self.joinProposalsInDataframe(listOfProposal)

            # if not isinstance(df, pd.DataFrame):
            #     return"Erro: A entrada não é um DataFrame válido."

            # for row in df.iterrows():
            #     if row[1]["COD_BANCO"] != "LEV":
            #         df.at[row[0], "VAL_COMISSAO"] = 0
            # df["NOM_BANCO"] = df["NOM_BANCO"].str.replace("_", " ")
            # df["TIPO_COMISSAO_BANCO"] = df["DSC_SITUACAO_BANCO"].map(COMISSAO_MAPPER).fillna("OUTROS")
            # df["DAT_CREDITO"] = pd.to_datetime(df["DAT_CREDITO"], unit="D", origin="1899-12-30")
            # df["DSC_TIPO_COMISSAO"] = ""
            # df["DSC_SITUACAO_BANCO"] = ""
            # df["COD_BANCO"] = ""
            # df["DSC_PRODUTO"] = ""

            logger.info("Processamento do c6bankcomissao finalizado com sucesso")
            return df
        except Exception:
            logger.exception("Erro ao editar c6bankcomissao")
            logger.error("Erro ao editar c6bankcomissao")
            return "Erro ao editar c6bankcomissao"
        finally:
            logger.info("Finalizado processo de edicao c6autocomissao")