import pandas as pd
import logging
from .bank import Bank
from ..utils import convertValues


logger = logging.getLogger("bancos")

class Presenca(Bank):
    def __init__(self, name = "PRESENCA BANK SCP", num = 482, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df, header=2)
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
               "PROPOSTA":"NUM_PROPOSTA",
               "DT PAGTO":"DAT_CREDITO",
               "VR BASE":"VAL_BASE_COMISSAO",
               "VR CMS":"VAL_COMISSAO",
               "% CMS":"PCL_COMISSAO",
            }

            length = len(df["PROPOSTA"])

            df = df.drop(index=[length -1])

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error


            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")

            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["NUM_BANCO"] = 482
            df_novo["NOM_BANCO"] = 'PRESENCA BANK SCP'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            for i in range(len(df_novo["VAL_BASE_COMISSAO"])):
                if df_novo["VAL_BASE_COMISSAO"][i] < 0:
                    df_novo.loc[i, "TIPO_COMISSAO_BANCO"] = 'ESTORNO'
                else:
                    df_novo.loc[i, "TIPO_COMISSAO_BANCO"] = 'DIRETA'

            logger.info("Processamento do Presenca finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Presenca")
            logger.error("Erro ao editar Presenca")
            return "Erro ao editar Presenca"
        finally:
            logger.info("Finalizado processo de edicao Presenca")