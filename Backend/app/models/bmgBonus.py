import pandas as pd
from ..utils import convertValues
from .bank import Bank
import logging

logger = logging.getLogger("bancos")

class BmgBonus(Bank):
    def __init__(self, name = "BMG", num = 701, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-BMG BONUS")
            df = pd.read_csv(df, sep=';')
            logger.info("Lido o arquivo do BMG BONUS")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.erro("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
           logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):
        try:
            df = self.readArchive(df)

            infos ={
                "Contrato/Apolice":"NUM_PROPOSTA",
                "Valor Base": "VAL_BASE_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()

            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["TIPO_COMISSAO_BANCO"] = "BÔNUS"
            df_novo["NUM_BANCO"] = 0
            df_novo["NOM_BANCO"] = 'BMG'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            return df_novo
        except Exception:
            logger.exception("Erro ao editar Bmg")
            logger.error("Erro ao editar Bmg")
            return "Erro ao editar Bmg"
        finally:
            logger.info("Finalizado processo de edicao Bmg")