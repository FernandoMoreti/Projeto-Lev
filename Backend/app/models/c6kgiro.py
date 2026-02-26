import pandas as pd
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class C6kgiro(Bank):
    def __init__(self, name = "C6 Kgiro", num = 3336, type = "excel"):
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


    def run(self, df):

        try:

            df = self.readArchive(df)

            infos = {
                "Proposta Consignado": "NUM_PROPOSTA",
                "Data Pagamento Kgiro": "DAT_CREDITO",
                "Prazo Kgiro": "QTD_PARCELA",
                "Valor Liberado Consignado": "VAL_BASE_COMISSAO",
                "% Comissão VF": "PCL_COMISSAO",
                "Valor Estimado Antecipação": "VAL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            df = df[df["Nome Corban"] == "LEV"]

            logger.info("Processamento do c6bankcomissao finalizado com sucesso")
            return df
        except Exception:
            logger.exception("Erro ao editar c6bankcomissao")
            logger.error("Erro ao editar c6bankcomissao")
            return "Erro ao editar c6bankcomissao"
        finally:
            logger.info("Finalizado processo de edicao c6autocomissao")