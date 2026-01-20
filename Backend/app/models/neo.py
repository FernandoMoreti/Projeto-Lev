import pandas as pd
from datetime import datetime
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Neo(Bank):
    def __init__(self, name = "NEO CREDITO", num = 3333333, type = "excel"):
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

            data = df.filename.split("_")[1].split(".")[0]
            resultado = f"{data[:2]}/{data[2:4]}/{data[4:]}"

            df = self.readArchive(df)

            infos ={
               "PROPOSTA":"NUM_PROPOSTA",
               "VALOR BRUTO":"VAL_BASE_COMISSAO",
               "CMS R$":"VAL_COMISSAO",
               "CMS %":"PCL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            tamanho = len(df_novo)

            df_novo = df_novo.drop(index=[tamanho -1, tamanho -2, tamanho -3, tamanho -4])

            df_novo["PCL_COMISSAO"] = round(df_novo["PCL_COMISSAO"] * 100, 2)

            df_novo["NUM_BANCO"] = 3333333
            df_novo["NOM_BANCO"] = "NEO CREDITO"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
            df_novo["DAT_CREDITO"] = resultado

            logger.info("Processamento do Neo finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Neo")
            logger.error("Erro ao editar Neo")
            return "Erro ao editar Neo"
        finally:
            logger.info("Finalizado processo de edicao Neo")