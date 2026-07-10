import pandas as pd
import logging
from .bank import Bank
import numpy as np
from ..utils import convertValues

logger = logging.getLogger("bancos")

class QueroMaisCartao(Bank):
    def __init__(self, name = "Quero Mais", num = 2222222, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_html(df, header=2)[0]
            df = df.iloc[:-3]
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
               "Nº Proposta":"NUM_PROPOSTA",
               "Data Base":"DAT_CREDITO",
               "Base de Cálculo":"VAL_BASE_COMISSAO",
               "Valor Comissão":"VAL_COMISSAO",
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

            df_novo["NUM_BANCO"] = 3030
            df_novo["NOM_BANCO"] = "QUERO MAIS CREDITO"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] / 10000
            df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"] / 100
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            listOfPcl = []

            for index, row in df_novo.iterrows():
                if row["VAL_COMISSAO"] == 0 and row["VAL_BASE_COMISSAO"] == 0:
                    listOfPcl.append(0)
                else:
                    listOfPcl.append((row["VAL_COMISSAO"] / row["VAL_BASE_COMISSAO"]) * 100)

            df_novo["PCL_COMISSAO"] = listOfPcl

            logger.info("Processamento do Quero mais credito finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Quero mais credito")
            logger.error("Erro ao editar Quero mais credito")
            return "Erro ao editar Quero mais credito"
        finally:
            logger.info("Finalizado processo de edicao Quero mais credito")