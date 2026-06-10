import pandas as pd
import logging
from .bank import Bank
import numpy as np

logger = logging.getLogger("bancos")

class Qualibank(Bank):
    def __init__(self, name = "QUALI BANK", num = 2222222, type = "excel"):
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

            infos ={
               "NUMERO_CTT":"NUM_PROPOSTA",
               "DATA_PAGAMENTO":"DAT_CREDITO",
               "VALOR_BASE":"VAL_BASE_COMISSAO",
               "VALOR_INCENTIVO":"VAL_COMISSAO",
               "PERC_INCENTIVO":"PCL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["TIPO_COMISSAO_BANCO"] = np.where(df["DESCRICAO"] == "BONUS CAMPANHA", "BONUS EXTRA", "DIRETA")

            df_novo["NUM_BANCO"] = 2222222
            df_novo["NOM_BANCO"] = "QUALI BANK"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]

            logger.info("Processamento do Qualibank finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Qualibank")
            logger.error("Erro ao editar Qualibank")
            return "Erro ao editar Qualibank"
        finally:
            logger.info("Finalizado processo de edicao Qualibank")