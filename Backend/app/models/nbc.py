import pandas as pd
from ..utils import convertValues
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Nbc(Bank):
    def __init__(self, name = "NBC BANK", num = 753, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df, header=10)
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
                "Base de Cálculo": "VAL_BASE_COMISSAO",
                "Valor da Comissão": "VAL_COMISSAO",
                "Percentual": "PCL_COMISSAO",
                "Data Base": "DAT_CREDITO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            length = len(df_novo["NUM_PROPOSTA"])
            df_novo = df_novo.drop(df_novo.index[length-1])
            df_novo = df_novo.drop(df_novo.index[length-2])
            df_novo = df_novo.drop(df_novo.index[length-3])

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")
            df_novo["PCL_COMISSAO"] = convertValues(df_novo, "PCL_COMISSAO")

            df_novo["NUM_BANCO"] = 753
            df_novo["NOM_BANCO"] = "NBC BANK"
            df_novo["NUM_PROPOSTA"] = df_novo["NUM_PROPOSTA"].astype(int)
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Nbc finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Nbc")
            logger.error("Erro ao editar Nbc")
            return "Erro ao editar Nbc"
        finally:
            logger.info("Finalizado processo de edicao Nbc")