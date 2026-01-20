import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Euro(Bank):
    def __init__(self, name = "EURO17 EMPRESARIAL", num = 359108, type = "excel"):
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

            infos = {
                "Proposta":"NUM_PROPOSTA",
                "Vlr. Liberado":"VAL_BASE_COMISSAO",
                "% Comissão":"PCL_COMISSAO",
                "Vlr. Comissão":"VAL_COMISSAO",
                "Dt. de Pagamento":"DAT_CREDITO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            tamanho = len(df_novo["NUM_PROPOSTA"])

            df_novo = df_novo.drop(index=[tamanho -1, tamanho -2])

            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(str).str.replace("%", "").astype(float)
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
            df_novo["NUM_BANCO"] = "359108"
            df_novo["NOM_BANCO"] = "EURO17 EMPRESARIAL"

            logger.info("Processamento do Euro finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Euro")
            logger.error("Erro ao editar Euro")
            return "Erro ao editar Euro"
        finally:
            logger.info("Finalizado processo de edicao Euro")