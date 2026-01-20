import pandas as pd
import logging
from pathlib import Path
from datetime import datetime, timedelta
from .bank import Bank

logger = logging.getLogger("bancos")

class V8(Bank):
    def __init__(self, name = "V8 DIGITAL", num = 1725, type = "excel"):
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
            logger.info("Iniciando processo de edicao do V8")

            df = self.readArchive(df)

            infos ={
                "NUM_PROPOSTA":"NUM_PROPOSTA",
                "DAT_CREDITO":"DAT_CREDITO",
                "VAL_BASE_COMISSAO":"VAL_BASE_COMISSAO",
                "VAL_COMISSAO_TOTAL":"VAL_COMISSAO",
                "PERCENTUAL_REPASSE_TOTAL":"PCL_COMISSAO",
                "NUM_CONTRATO": "NUM_CONTRATO",
                "COD_PRODUTO" : "COD_PRODUTO",
                "DSC_PRODUTO" : "DSC_PRODUTO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            if"NUM_PROPOSTA"in df.columns:
                df["NUM_PROPOSTA"] = df["NUM_PROPOSTA"].astype(str)

            df_novo["NUM_BANCO"] = '1725'
            df_novo["NOM_BANCO"] = 'V8 DIGITAL'
            df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'

            logger.info("Processamento do V8 finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar V8")
            logger.error("Erro ao editar V8")
            return "Erro ao editar V8"
        finally:
            logger.info("Finalizado processo de edicao V8")