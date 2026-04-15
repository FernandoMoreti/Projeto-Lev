import pandas as pd
import logging
from .bank import Bank
import numpy as np
from datetime import datetime

logger = logging.getLogger("bancos")

class C6auto(Bank):
    def __init__(self, name = "C6 AUTO", num = 3336, type = "excel"):
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
                "Cd Contrato": "NUM_PROPOSTA",
                "R$ Principal Ajustado (TXE)": "VAL_BASE_COMISSAO",
                "R$ Comissão À Vista Bruto - Master": "VAL_COMISSAO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["PCL_COMISSAO"] = np.where(
                df_novo["VAL_BASE_COMISSAO"] == 0,
                0,
                (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100
            )
            df_novo["NUM_BANCO"] = 3336
            df_novo["NOM_BANCO"] = 'C6 AUTO'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
            df_novo["DAT_CREDITO"] = datetime.now()
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100

            logger.info("Processamento do c6auto finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar c6auto")
            logger.error("Erro ao editar c6auto")
            return "Erro ao editar c6auto"
        finally:
            logger.info("Finalizado processo de edicao c6auto")