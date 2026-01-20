import pandas as pd
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Phtech(Bank):
    def __init__(self, name = "PHTECH", num = 8768, type = "csv"):
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

            df = self.readArchive(df)

            infos ={
               "COD. BANCO":"NUM_PROPOSTA",
               "DATA PG. CORRETOR":"DAT_CREDITO",
               "VALOR LIQUIDO":"VAL_BASE_COMISSAO",
               "COMISSAO":"VAL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["NUM_BANCO"] = 8768
            df_novo["NOM_BANCO"] = "PHTECH"
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Phtech finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Phtech")
            logger.error("Erro ao editar Phtech")
            return "Erro ao editar Phtech"
        finally:
            logger.info("Finalizado processo de edicao Phtech")