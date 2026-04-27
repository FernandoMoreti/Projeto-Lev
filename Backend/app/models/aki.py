import pandas as pd
from ..utils import validDf
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Aki(Bank):

    def __init__(self, name="AKI CAPITAL", num = 1684, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-Aki")

            data = df.filename.split("_")[0]
            diaMesAno = f"{data[:2]}/{data[3:5]}/{data[6:10]}"

            df = pd.read_excel(df)

            logger.info("Lido o arquivo do Aki")
            return df, diaMesAno
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.erro("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):
        try:
            df, diaMesAno = self.readArchive(df)

            infos = {
                "Nº Contrato": "NUM_PROPOSTA",
                "Valor Total": "VAL_BASE_COMISSAO",
                "% Prêmio": "PCL_COMISSAO",
                "Valor Prêmio": "VAL_COMISSAO",
            }
            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error
            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            logger.info("Dataframe criado com sucesso")
            logger.info("Adicionando valores de forma fixa")

            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100
            df_novo["DAT_CREDITO"] = diaMesAno
            df_novo["NUM_BANCO"] = 1684
            df_novo["NOM_BANCO"] = "AKI CAPITAL"

            return df_novo
        except Exception:
            logger.exception("Erro ao editar Aki")
            logger.error("Erro ao editar Aki")
            return "Erro ao editar Aki"
        finally:
            logger.info("Finalizado processo de edicao AKi")
