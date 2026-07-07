import pandas as pd
import logging
from .bank import Bank
from ..utils import convertValues

logger = logging.getLogger("bancos")

class Vctex(Bank):
    def __init__(self, name = "VCTEX CORRESPONDENTE", num = 1530, type = "csv"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_csv(df, sep=";")
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
               "Número do Contrato":"NUM_PROPOSTA",
               "Valor Liberado":"VAL_BASE_COMISSAO",
               "Data de Repasse Comissão": "DAT_CREDITO",
               "Valor Comissão":"VAL_COMISSAO",
               "% Comissão":"PCL_COMISSAO",
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
            df_novo["PCL_COMISSAO"] = convertValues(df_novo, "PCL_COMISSAO")

            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["NUM_BANCO"] = 1530
            df_novo["NOM_BANCO"] = "VCTEX CORRESPONDENTE"
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Vctex finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Vctex")
            logger.error("Erro ao editar Vctex")
            return "Erro ao editar Vctex"
        finally:
            logger.info("Finalizado processo de edicao Vctex")