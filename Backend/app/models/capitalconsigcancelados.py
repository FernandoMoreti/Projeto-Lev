import pandas as pd
from datetime import datetime
import requests
from ..utils import convertValues
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class CapitalConsigCancelados(Bank):
    def __init__(self, name = "QUERO MAIS CREDITO", num = 3030, type = "excel"):
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
            logger.info("Iniciando processo de edicao do Queromaiscancelados")

            df = self.readArchive(df)

            infos = {
               "CONTRATO":"NUM_PROPOSTA",
               "Valor Prêmio":"VAL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            list_val_bruto = []

            for prop in df_novo["NUM_PROPOSTA"]:
                data = requests.get(f"http://192.168.1.252:3004/v1/wb-api/proposta/?proposal={prop}")
                if data:
                    result = data.json()
                    list_val_bruto.append(result[0]["bruto"])

            df_novo["VAL_BRUTO"] = list_val_bruto

            df_novo["VAL_BRUTO"] = convertValues(df_novo, "VAL_BRUTO")

            df_novo["NUM_BANCO"] = 12222222
            df_novo["NOM_BANCO"] = 'CAPITAL CONSIG'
            df_novo["DAT_CREDITO"] = datetime.now().date()
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BRUTO"]
            df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BRUTO"]
            df_novo["PCL_COMISSAO"] = df_novo["VAL_COMISSAO"] / df_novo["VAL_BRUTO"] * 100
            df_novo["TIPO_COMISSAO_BANCO"] = 'ESTORNO'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            logger.info("Processamento do Queromaiscancelados finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Queromaiscancelados")
            logger.error("Erro ao editar Queromaiscancelados")
            return "Erro ao editar Queromaiscancelados"
        finally:
            logger.info("Finalizado processo de edicao Queromaiscancelados")