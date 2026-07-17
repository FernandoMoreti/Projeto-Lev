import pandas as pd
from datetime import datetime
from ..utils import createDataframe, inputValueColumns, validDf
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Empresteicred(Bank):
    def __init__(self, name = "EMPRESTEI CARD", num = 1708, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df)
            df = df.iloc[:-1]
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

            print(df.columns)

            infos = {
                "Operação ": "NUM_PROPOSTA",
                "Líquido": "VAL_BASE_COMISSAO",
                "comissão": "PCL_COMISSAO",
                "Valor ": "VAL_COMISSAO",
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

            df_novo["NUM_BANCO"] = '1708'
            df_novo["NOM_BANCO"] = 'EMPRESTEI CARD'
            df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["DAT_CREDITO"] = datetime.now().date()
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100

            logger.info("Processamento do Empresteicred finalizado com sucesso")
            df_novo = df_novo[pd.notna(df_novo["NUM_PROPOSTA"])]
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Empresteicred")
            logger.error("Erro ao editar Empresteicred")
            return "Erro ao editar Empresteicred"
        finally:
            logger.info("Finalizado processo de edicao Empresteicred")


