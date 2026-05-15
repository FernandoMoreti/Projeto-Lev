import pandas as pd
import logging
from .bank import Bank
from ..utils import convertValues

logger = logging.getLogger("bancos")

class Nyc(Bank):
    def __init__(self, name = "NYC BANK", num = 1728, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df)
            df = df.iloc[:-3]
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
               "Id":"NUM_PROPOSTA",
               "Data de Pagamento Comissão":"DAT_CREDITO",
               "Valor Líquido":"VAL_BASE_COMISSAO",
               "$ Comissão Promotora":"VAL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")
            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")

            df_novo["NUM_BANCO"] = '1728'
            df_novo["NOM_BANCO"] = 'NYC BANK'
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"])
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            if"PCL_COMISSAO"in df_novo.columns:
                df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

            logger.info("Processamento do Nyc finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Nyc")
            logger.error("Erro ao editar Nyc")
            return "Erro ao editar Nyc"
        finally:
            logger.info("Finalizado processo de edicao Nyc")