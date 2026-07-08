import pandas as pd
from ..utils import convertValues
from .bank import Bank
import logging

logger = logging.getLogger("bancos")

class PanLafy(Bank):
    def __init__(self, name = "PANLAFY", num = 701, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-PANLAFY")
            df = pd.read_excel(df, header=1)
            df = df.iloc[:-1]
            logger.info("Lido o arquivo do PANLAFY")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.erro("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
           logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:

            df = self.readArchive(df)

            infos ={
                "PROPOSTA": "NUM_PROPOSTA",
                "DT PAGTO": "DAT_CREDITO",
                "VR BASE": "VAL_BASE_COMISSAO",
                "VR CMS": "VAL_COMISSAO",
                "TIPO CMS": "TIPO_COMISSAO_BANCO",
                "% CMS": "PCL_COMISSAO"
            }

            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            df_novo = self.createDataframe()

            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")

            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["NUM_BANCO"] = 623333
            df_novo["NOM_BANCO"] = 'PAN LAFY'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            types = []

            for type in df_novo["TIPO_COMISSAO_BANCO"]:
                if type == "BÔNUS_CAMPANHA":
                    type = "BONUS EXTRA"
                if type == "AD_DIF":
                    type = "ANTECIPAÇÃO"
                types.append(type)

            df_novo["TIPO_COMISSAO_BANCO"] = types

            return df_novo
        except Exception:
            logger.exception("Erro ao editar PANLAFY")
            logger.error("Erro ao editar PANLAFY")
            return "Erro ao editar PANLAFY"
        finally:
            logger.info("Finalizado processo de edicao PANLAFY")