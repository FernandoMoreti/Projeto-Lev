import pandas as pd
import logging
from datetime import datetime
from .bank import Bank

logger = logging.getLogger("bancos")

class CapitalConsigComissao(Bank):
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
            logger.info("Iniciando processo de edicao do Queromaiscomissao")

            df = self.readArchive(df)

            infos = {
               "NR.PROP.":"NUM_PROPOSTA",
               "VLR TOTAL PRODUCUÇÃO (VLR LIQUIDO + SEGURO)":"VAL_BASE_COMISSAO",
               "Valor Prêmio":"VAL_COMISSAO",
               "% Prêmio":"PCL_COMISSAO",
               "Dt Pag Prêmio": "DAT_CREDITO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["NUM_BANCO"] = 12222222
            df_novo["NOM_BANCO"] = 'CAPITAL CONSIG'
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100
            df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            logger.info("Processamento do Queromaiscomissao finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Queromaiscomissao")
            logger.error("Erro ao editar Queromaiscomissao")
            return "Erro ao editar Queromaiscomissao"
        finally:
            logger.info("Finalizado processo de edicao Queromaiscomissao")