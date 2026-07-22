import pandas as pd
from ..utils import convertValues
from .bank import Bank
import logging
from ..mapper import DAYCOVAL

logger = logging.getLogger("bancos")

class DaycovalCartao(Bank):
    def __init__(self, name = "BANCO DAYCOVAL S.A.", num = 707, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-Daycoval Cartao")
            df = pd.read_html(df, header=2)[0]
            df = df.iloc[:-3]
            logger.info("Lido o arquivo do Daycoval Cartao")
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
                "Nº Proposta": "NUM_PROPOSTA",
                "Data Base": "DAT_CREDITO",
                "Base de Cálculo": "VAL_BASE_COMISSAO",
                "Valor Comissão": "VAL_COMISSAO",
                "Tp. Oper.": "TIPO_COMISSAO_BANCO",
            }

            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            df_novo = self.createDataframe()

            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] / 10000
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")
            df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"] / 100

            listOfPorcent = []

            for index, row in df_novo.iterrows():
                if row["VAL_BASE_COMISSAO"] == 0 or row["VAL_COMISSAO"] ==0:
                    listOfPorcent.append(0)
                else:
                    listOfPorcent.append((row["VAL_COMISSAO"] / row["VAL_BASE_COMISSAO"]) * 100)

            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["NUM_BANCO"] = 707
            df_novo["NOM_BANCO"] = 'BANCO DAYCOVAL S.A.'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["PCL_COMISSAO"] = listOfPorcent

            list_types = []

            for index, row in df_novo.iterrows():
                type_row = DAYCOVAL[row["TIPO_COMISSAO_BANCO"].upper()]
                list_types.append(type_row)

            df_novo["TIPO_COMISSAO_BANCO"] = list_types

            return df_novo
        except Exception:
            logger.exception("Erro ao editar Daycoval Cartao")
            logger.error("Erro ao editar Daycoval Cartao")
            return "Erro ao editar Daycoval Cartao"
        finally:
            logger.info("Finalizado processo de edicao Daycoval Cartao")