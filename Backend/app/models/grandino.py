import pandas as pd
import logging
from ..utils import convertValues
from .bank import Bank

logger = logging.getLogger("bancos")

class Grandino(Bank):
    def __init__(self, name = "GRANDINO LTDA", num = 88888, type = "csv"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_csv(df, sep=";")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do Grandino")

            df = self.readArchive(df)

            infos ={
               "Nro Proposta":"NUM_PROPOSTA",
               "Data de Fechamento":"DAT_CREDITO",
               "Base de Cálculo":"VAL_BASE_COMISSAO",
               "Valor Comissão":"VAL_COMISSAO",
               "Porcentagem":"PCL_COMISSAO"
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

            df_novo["NUM_BANCO"] = '88888'
            df_novo["NOM_BANCO"] = 'GRANDINO LTDA'
            df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            logger.info("Processamento do Grandino finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Grandino")
            logger.error("Erro ao editar Grandino")
            return "Erro ao editar Grandino"
        finally:
            logger.info("Finalizado processo de edicao Grandino")