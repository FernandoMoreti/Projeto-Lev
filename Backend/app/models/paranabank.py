import pandas as pd
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Paranabank(Bank):
    def __init__(self, name = "PARANÁ BANCO S.A.", num = 254, type = "excel"):
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
                "Nr. Proposta": "NUM_PROPOSTA",
                "Data Fatura": "DAT_CREDITO",
                "Valor base": "VAL_BASE_COMISSAO",
                "% Comissão": "PCL_COMISSAO",
                "Valor comissão": "VAL_COMISSAO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["NUM_BANCO"] = 254
            df_novo["NOM_BANCO"] = "PARANÁ BANCO S.A."
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["NUM_BANCO"] = 254
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Paranabank finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Paranabank")
            logger.error("Erro ao editar Paranabank")
            return "Erro ao editar Paranabank"
        finally:
            logger.info("Finalizado processo de edicao Paranabank")