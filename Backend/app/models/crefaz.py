import pandas as pd
import logging
from datetime import datetime
from .bank import Bank
from ..utils import convertValues

logger = logging.getLogger("bancos")

class Crefaz(Bank):
    def __init__(self, name = "CREFAZ", num = 1964, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df.stream, engine='xlrd', header=0)
            df = df.iloc[:-4]
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do Crefaz")

            df = self.readArchive(df)

            infos = {
               "Código Proposta": "NUM_PROPOSTA",
               "Vlr. Operação": "VAL_BASE_COMISSAO",
               "R$ Comissão": "VAL_COMISSAO",
               "DT Aceite": "DAT_CREDITO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")

            df_novo["NUM_BANCO"] = 1964
            df_novo["NOM_BANCO"] = 'CREFAZ'
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_BASE_COMISSAO"] / df_novo["VAL_COMISSAO"])
            df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            logger.info("Processamento do Crefaz finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Crefaz")
            logger.error("Erro ao editar Crefaz")
            return "Erro ao editar Crefaz"
        finally:
            logger.info("Finalizado processo de edicao Crefaz")