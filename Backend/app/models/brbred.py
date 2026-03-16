import pandas as pd
from ..utils import convertValues
from .bank import Bank
import logging

logger = logging.getLogger("bancos")

class BrbRed(Bank):
    def __init__(self, name = "BRB", num = 701, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-BRB360")
            df = pd.read_excel(df)
            logger.info("Lido o arquivo do BRB360")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.erro("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
           logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:

            df = self.readArchive(df)

            infos ={
                "num_proposta": "NUM_PROPOSTA",
                "movdatapagamento": "DAT_CREDITO",
                "valor_contrato": "VAL_BASE_COMISSAO",
                "valor_comissao": "VAL_COMISSAO",
                "emppercent_agenciador": "PCL_COMISSAO"
            }

            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            df_novo = self.createDataframe()

            df_novo = self.inputValues(df, df_novo, infos)

            if pd.api.types.is_numeric_dtype(df_novo["DAT_CREDITO"]):
                df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], unit='D', origin='1899-12-30')
            else:
                df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], errors='coerce')

            df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime('%Y-%m-%d')

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")

            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["NUM_BANCO"] = 702
            df_novo["NOM_BANCO"] = 'BRB - RED'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            return df_novo
        except Exception:
            logger.exception("Erro ao editar Brb360")
            logger.error("Erro ao editar Brb360")
            return "Erro ao editar Brb360"
        finally:
            logger.info("Finalizado processo de edicao Brb360")