import pandas as pd
import logging
from datetime import datetime
from .bank import Bank

logger = logging.getLogger("bancos")

class Webcash(Bank):
    def __init__(self, name = "WEBCASH", num = 1730, type = "excel"):
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
            logger.info("Iniciando processo de edicao do Webcash")

            df = self.readArchive(df)

            data = datetime.now().strftime("%d/%m/%Y")

            infos ={
               "PROPOSTA":"NUM_PROPOSTA",
               "SEGURO":"VAL_BRUTO",
               "LIQUIDO":"VAL_LIQUIDO",
               "COMISSÃO":"VAL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BRUTO"] + df_novo["VAL_LIQUIDO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100
            df_novo["NOM_BANCO"] = "WEBCASH"
            df_novo["NUM_BANCO"] = 1730
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["DAT_CREDITO"] = data
            df_novo["VAL_BRUTO"] = ""

            logger.info("Processamento do Webcash finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Webcash")
            logger.error("Erro ao editar Webcash")
            return "Erro ao editar Webcash"
        finally:
            logger.info("Finalizado processo de edicao Webcash")

