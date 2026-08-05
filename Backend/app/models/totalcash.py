import pandas as pd
import logging
from datetime import datetime
from ..utils import convertValues
from .bank import Bank

logger = logging.getLogger("bancos")

class Totalcash(Bank):
    def __init__(self, name = "TOTALCASH", num = 1731, type = "excel"):
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
            logger.info("Iniciando processo de edicao do Totalcash")

            df = self.readArchive(df)

            infos = {
                "Nr Proposta": "NUM_PROPOSTA",
                "Valor Liberado Cliente": "VAL_BASE_COMISSAO",
                "Valor Comissão": "VAL_COMISSAO",
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

            df_novo["NUM_BANCO"] = 1731
            df_novo["NOM_BANCO"] = "TOTALCASH"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["DAT_CREDITO"] = datetime.now().date()
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100

            listOfTypes = []

            for index, row in df_novo.iterrows():
                if row["VAL_COMISSAO"] < 0:
                    listOfTypes.append("ESTORNO")
                else:
                    listOfTypes.append("DIRETA")

            df_novo["TIPO_COMISSAO_BANCO"] = listOfTypes
            df_novo["DAT_CREDITO"] = pd.to_datetime(df_novo["DAT_CREDITO"], errors='coerce').dt.strftime('%d/%m/%Y')

            logger.info("Processamento do Totalcash finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Totalcash")
            logger.error("Erro ao editar Totalcash")
            return "Erro ao editar Totalcash"
        finally:
            logger.info("Finalizado processo de edicao Totalcash")