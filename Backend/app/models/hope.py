import pandas as pd
from ..utils import convertValues
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Hope(Bank):
    def __init__(self, name = "HOPE", num = 1597, type = "html"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df, header=0)
            df = df[pd.notna(df["Valor Base do Contrato"])]
            df = df.iloc[:-1]
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
                "Número Ade":"NUM_PROPOSTA",
                "Data do Fechamento":"DAT_CREDITO",
                "Valor Bruto":"VAL_BASE_COMISSAO",
                "% Comissão": "PCL_COMISSAO",
                "Valor":"VAL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            tamanho = len(df_novo["NUM_PROPOSTA"])

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")

            df_novo["NOM_BANCO"] = "HOPE"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["NUM_BANCO"] = 1597

            listOfTypes = []
            listOfVal = []

            for index, row in df_novo.iterrows():
                if row["VAL_COMISSAO"] < 0:
                    listOfTypes.append("ESTORNO")
                    listOfVal.append(row["VAL_COMISSAO"])
                else:
                    listOfTypes.append("DIRETA")
                    listOfVal.append(row["VAL_COMISSAO"])

            df_novo["VAL_COMISSAO"] = listOfVal
            df_novo["TIPO_COMISSAO_BANCO"] = listOfTypes
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100

            logger.info("Processamento do Hope finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Hope")
            logger.error("Erro ao editar Hope")
            return "Erro ao editar Hope"
        finally:
            logger.info("Finalizado processo de edicao Hope")