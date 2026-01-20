import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Icred(Bank):
    def __init__(self, name = "ICRED", num = 329, type = "excel"):
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
               "Number":"NUM_PROPOSTA",
               "Data":"DAT_CREDITO",
               "commission_base":"VAL_BASE_COMISSAO",
               "commission_factor": "PCL_COMISSAO",
               "commission_value":"VAL_COMISSAO",
               "commission_type":"TIPO_COMISSAO_BANCO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["NUM_BANCO"] = '329'
            df_novo["NOM_BANCO"] = 'ICRED'
            df_novo["TIPO_COMISSAO_BANCO"] = df_novo["TIPO_COMISSAO_BANCO"].replace('Flat', 'DIRETA')
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(float) * 100

            logger.info("Processamento do Icred finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Icred")
            logger.error("Erro ao editar Icred")
            return "Erro ao editar Icred"
        finally:
            logger.info("Finalizado processo de edicao Icred")