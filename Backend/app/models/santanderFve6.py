import pandas as pd
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Santanderfvevi(Bank):
    def __init__(self, name = "SANTANDER", num = 351, type = "csv"):
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
            logger.info("Iniciando processo de edicao do Santanderfvevi")

            df = self.readArchive(df)

            infos = {
                "Proposta": "NUM_PROPOSTA",
                "Valor Bruto": "VAL_BASE_COMISSAO",
                "Percentual Comissão": "PCL_COMISSAO",
                "Valor Total Comissão": "VAL_COMISSAO",
                "Data do Cálculo": "DAT_CREDITO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
            df_novo["NUM_BANCO"] = 351
            df_novo["NOM_BANCO"] = "SANTANDER"
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Santanderfvevi finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Santanderfvevi")
            logger.error("Erro ao editar Santanderfvevi")
            return "Erro ao editar Santanderfvevi"
        finally:
            logger.info("Finalizado processo de edicao Santanderfvevi")