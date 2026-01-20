import pandas as pd
import logging
from ..utils import convertValues
from .bank import Bank

logger = logging.getLogger("bancos")

class Safracomissaozero(Bank):
    def __init__(self, name = "Safra", num = 42, type = "csv"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_csv(df, sep=';')
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do Safracomissaozero")

            df = self.readArchive(df)

            infos = {
                "Contrato": "NUM_PROPOSTA",
                "Valor Principal": "VAL_BASE_COMISSAO",
                "Data efetivacao Contrato": "DAT_CREDITO",
                "CPF": "COD_CPF_CLIENTE",
                "Nome Cliente": "NOM_CLIENTE",
                "Nome Tabela Juros": "DSC_PRODUTO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")

            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["NOM_BANCO"] = "Safra"
            df_novo["NUM_BANCO"] = 42
            df_novo["TIPO_COMISSAO_BANCO"] = "AUTORREGULAÇAO"

            logger.info("Processamento do Safracomissaozero finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Safracomissaozero")
            logger.error("Erro ao editar Safracomissaozero")
            return "Erro ao editar Safracomissaozero"
        finally:
            logger.info("Finalizado processo de edicao Safracomissaozero")