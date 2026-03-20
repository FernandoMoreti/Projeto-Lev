import pandas as pd
import logging
from datetime import datetime
from .bank import Bank

logger = logging.getLogger("bancos")

class Caixa(Bank):
    def __init__(self, name = "CAIXA", num = 104, type = "excel"):
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
                "Nr Proposta":"NUM_PROPOSTA",
                "Valor Liberado Cliente":"VAL_BASE_COMISSAO",
                "% Comissao":"PCL_COMISSAO",
                "Valor Nota Fiscal":"VAL_COMISSAO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            date = datetime.now()

            df_novo["NOM_BANCO"] = "CAIXA"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["NUM_BANCO"] = 104
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100
            df_novo["DAT_CREDITO"] = date

            logger.info("Processamento do Caixa finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Caixa")
            logger.error("Erro ao editar Caixa")
            return "Erro ao editar Caixa"
        finally:
            logger.info("Finalizado processo de edicao Caixa")