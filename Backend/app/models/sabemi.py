import pandas as pd
import logging
from ..utils import convertValues
from .bank import Bank

logger = logging.getLogger("bancos")

class Sabemi(Bank):
    def __init__(self, name = "Safra", num = 42, type = "csv"):
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
            logger.info("Iniciando processo de edicao do Sabemi")

            df = self.readArchive(df)

            infos = {
                "Proposta": "NUM_PROPOSTA",
                "Valor AF Bruto": "VAL_BASE_COMISSAO",
                "Comissão": "VAL_COMISSAO",
                "Data Liberacao": "DAT_CREDITO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")

            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100
            df_novo["NOM_BANCO"] = "SABEMI"
            df_novo["NUM_BANCO"] = 5
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Sabemi finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Sabemi")
            logger.error("Erro ao editar Sabemi")
            return "Erro ao editar Sabemi"
        finally:
            logger.info("Finalizado processo de edicao Sabemi")