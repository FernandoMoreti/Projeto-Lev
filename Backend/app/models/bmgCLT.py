import pandas as pd
from ..utils import convertValues
from .bank import Bank
import logging

logger = logging.getLogger("bancos")

class BmgCLT(Bank):
    def __init__(self, name = "BMG", num = 701, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-BRB360")
            df = pd.read_csv(df, sep=';')
            logger.info("Lido o arquivo do BRB360")
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

            bruto = df["Valor Bruto"].astype(str).str.replace(",", ".").replace("nan", "0").astype(float)
            base = df["Valor Base"].astype(str).str.replace(",", ".").replace("nan", "0").astype(float)

            for index, row in df.iterrows():
                if row["Observacao"] != "":
                    row["% de Comissao"] = (bruto / base) * 100
                    row["Tipo de Comissao"] = "0 - OPERAÇÕES NORMAIS - USO DE FORMULÁRIOS"

            return df
        except Exception:
            logger.exception("Erro ao editar Bmg")
            logger.error("Erro ao editar Bmg")
            return "Erro ao editar Bmg"
        finally:
            logger.info("Finalizado processo de edicao Bmg")