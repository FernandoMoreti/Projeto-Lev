import pandas as pd
from ..utils import convertValues
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class NovosaqueCF(Bank):
    def __init__(self, name = "NOVO SAQUE", num = 1234, type = "csv"):
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

            infos = {
                "Contrato": "NUM_PROPOSTA",
                "R$ Liberado": "VAL_BASE_COMISSAO",
                "R$ CORBAN": "VAL_COMISSAO",
                "Pgto Comissão": "DAT_CREDITO",
                "Taxa de Juros": "PCL_TAXA_EMPRESTIMO"
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


            df_novo["NUM_BANCO"] = 1234
            df_novo["NOM_BANCO"] = "NOVO SAQUE"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Novosaque finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Novosaque")
            logger.error("Erro ao editar Novosaque")
            return "Erro ao editar Novosaque"
        finally:
            logger.info("Finalizado processo de edicao Novosaque")
