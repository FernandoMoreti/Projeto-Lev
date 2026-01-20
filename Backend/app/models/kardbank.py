import pandas as pd
from ..utils import convertValues
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Kardbank(Bank):
    def __init__(self, name = "KARDBANK", num = 6910, type = "html"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_html(df, header=0)[0]
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
                "Número Ade":"NUM_PROPOSTA",
                "Data Pgto Vendedor":"DAT_CREDITO",
                "Valor Bruto":"VAL_BASE_COMISSAO",
                "% Comissão":"PCL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")

            df_novo["NOM_BANCO"] = "KARDBANK"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] * (df_novo["PCL_COMISSAO"] / 100)
            df_novo["NUM_BANCO"] = 6910
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Kardbank finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Kardbank")
            logger.error("Erro ao editar Kardbank")
            return "Erro ao editar Kardbank"
        finally:
            logger.info("Finalizado processo de edicao Kardbank")