import pandas as pd
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Digio(Bank):
    def __init__(self, name="BANCO DIGIO", num=335, type="csv"):
        super().__init__(name, num, type)

    def readArchive(self, file_path):
        try:
            df = pd.read_csv(file_path, sep=";")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, file_path):
        try:
            logger.info("Iniciando processo de edicao do Digio")
            df = self.readArchive(file_path)
            if isinstance(df, str):
                return df
            infos = {
                "Prop.": "NUM_PROPOSTA",
                "Base de Cálculo": "VAL_BASE_COMISSAO",
                "Valor Comiss": "VAL_COMISSAO",
                "Parâm": "PCL_COMISSAO",
                "Dt. Pgto Cmss.": "DAT_CREDITO",
            }
            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error
            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)
            df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str).str.replace(".", "").str.replace(",", ".").astype(float)
            df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
            df_novo["NUM_BANCO"] = 335
            df_novo["NOM_BANCO"] = "BANCO DIGIO"
            df_novo["PCL_COMISSAO"] = (df_novo["PCL_COMISSAO"].astype(str).str.replace(",", ".").astype(float) * 100)
            logger.info("Processamento do Digio finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Digio")
            logger.error("Erro ao editar Digio")
            return "Erro ao editar Digio"
        finally:
            logger.info("Finalizado processo de edicao Digio")