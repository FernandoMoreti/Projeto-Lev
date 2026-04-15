import pandas as pd
import logging
from .bank import Bank
from datetime import datetime

logger = logging.getLogger("bancos")

class Viacerta(Bank):
    def __init__(self, name = "Viacerta", num = 7675, type = "csv"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df, header=8)
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do Vctex")

            df = self.readArchive(df)
            if isinstance(df, str):
                return df

            infos ={
               "NÚMERO DO CONTRATO":"NUM_PROPOSTA",
               "VALOR BASE":"VAL_BASE_COMISSAO",
               "VALOR DA COMISSÃO":"VAL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"] * 100)
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["NUM_BANCO"] = 7675
            df_novo["NOM_BANCO"] = "VIACERTA BANKING"
            df_novo["DAT_CREDITO"] = datetime.now()
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            print(df_novo)

            logger.info("Processamento do Vctex finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Vctex")
            logger.error("Erro ao editar Vctex")
            return "Erro ao editar Vctex"
        finally:
            logger.info("Finalizado processo de edicao Vctex")