import pandas as pd
from datetime import datetime
from ..utils import convertValues
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Bv(Bank):
    def __init__(self, name = "BV", num = 44, type = "excel"):
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

            infos ={
                "NUM_PROPOSTA":"NUM_PROPOSTA",
                "NUM_CONTRATO":"NUM_CONTRATO",
                "VAL_LIQUIDO": "VAL_BASE_COMISSAO",
                "VAL_COMISSAO":"VAL_COMISSAO"
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

            data = datetime.now().strftime("%d/%m/%Y")

            df_novo["DAT_CREDITO"] = data
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"] * 100)
            df_novo["NUM_BANCO"] = 44
            df_novo["NOM_BANCO"] = 'BV'
            df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'

            logger.info("Processamento do BV finalizado com sucesso")
            return df_novo

        except Exception:
            logger.exception("Erro ao editar BV")
            logger.error("Erro ao editar BV")
            return "Erro ao editar BV"
        finally:
            logger.info("Finalizado processo de edicao BV")