import pandas as pd
import logging
from .bank import Bank
from ..utils import convertValues

logger = logging.getLogger("bancos")

class Santanderolewl(Bank):
    def __init__(self, name = "BANCO OLE", num = 218, type = "csv"):
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
            logger.info("Iniciando processo de edicao do Santanderolewl")

            df = self.readArchive(df)

            infos ={
               "Proposta": "NUM_PROPOSTA",
               "Valor Líquido": "VAL_BASE_COMISSAO",
               "Valor Total Comissão": "VAL_COMISSAO",
               "Percentual Comissão": "PCL_COMISSAO",
               "Data do Cálculo": "DAT_CREDITO",
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
            df_novo["PCL_COMISSAO"] = convertValues(df_novo, "PCL_COMISSAO")

            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
            df_novo["NUM_BANCO"] = 218
            df_novo["NOM_BANCO"] = "BANCO OLE"

            logger.info("Processamento do Santanderolewl finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Santanderolewl")
            logger.error("Erro ao editar Santanderolewl")
            return "Erro ao editar Santanderolewl"
        finally:
            logger.info("Finalizado processo de edicao Santanderolewl")