import pandas as pd
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class C6equity(Bank):
    def __init__(self, name = "C6 BANK", num = 336, type = "excel"):
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
            logger.info("Iniciando processo de edicao do C6equity")

            df = self.readArchive(df)

            infos = {
                "CD CONTRATO": "NUM_PROPOSTA",
                "DT PRODUÇÃO": "DAT_CREDITO",
                "VL PRINCIPAL": "VAL_BASE_COMISSAO",
                "PC COMISSAO FLAT": "PCL_COMISSAO",
                "VALOR COMISSAO": "VAL_COMISSAO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["NUM_BANCO"] = 336
            df_novo["NOM_BANCO"] = 'C6 BANK'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100

            logger.info("Processamento do C6equity finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar C6equity")
            logger.error("Erro ao editar C6equity")
            return "Erro ao editar C6equity"
        finally:
            logger.info("Finalizado processo de edicao C6equity")