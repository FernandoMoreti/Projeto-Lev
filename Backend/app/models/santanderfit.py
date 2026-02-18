import pandas as pd
import logging
from .bank import Bank
from ..utils import convertValues

logger = logging.getLogger("bancos")

class Santanderfit(Bank):
    def __init__(self, name = "FIT ECONOMIA DE ENERGIA S.A.", num = 9173, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df, header=1)
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do Santanderfit")

            df = self.readArchive(df)

            infos ={
                "Nº da Instalação":"NUM_PROPOSTA",
                "Valor a Receber":"VAL_COMISSAO",
                "Percentual (%)":"PCL_COMISSAO",
                "Valor Base (R$)":"VAL_BASE_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            valores_tratados = []

            for valor in df_novo["VAL_BASE_COMISSAO"]:

                valor_str = str(valor)

                valor_teste = valor_str.replace(".", "")
                valor_teste = valor_teste[:3] + "." + valor_teste[3:]
                valor_str = float(valor_teste)

                valores_tratados.append(valor_str)

            df_novo["VAL_COMISSAO"] = valores_tratados

            valores_tratados = []

            for valor in df_novo["VAL_COMISSAO"]:
                valor_str = str(valor)

                valor_teste = valor_str.replace("R$", "")
                valor_teste = valor_teste.replace(" ", "")
                valor_teste = valor_teste.replace(".", "")
                valor_teste = valor_teste.replace(",", ".")
                valor_str = float(valor_teste)

                valores_tratados.append(valor_str)

            df_novo["VAL_COMISSAO"] = valores_tratados

            df_novo["NOM_BANCO"] = "FIT ECONOMIA DE ENERGIA S.A."
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["NUM_BANCO"] = 9173
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Santanderfit finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Santanderfit")
            logger.error("Erro ao editar Santanderfit")
            return "Erro ao editar Santanderfit"
        finally:
            logger.info("Finalizado processo de edicao Santanderfit")