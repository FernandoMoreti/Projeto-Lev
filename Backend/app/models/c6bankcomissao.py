import pandas as pd
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class C6bankcomissao(Bank):
    def __init__(self, name = "C6 BANK COMISSAO", num = 0, type = "excel"):  # num não especificado, coloquei 0
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
            logger.info("Iniciando processo de edicao do C6bankcomissao")

            df = self.readArchive(df)
            if isinstance(df, str):
                return df

            validNames = ["PACOTE"]

            for i, row in df.iterrows():
                if row["Nome Comissionado"] != "LEV":
                    df.at[i, "Vlr Bruto"] = 0

                if any(name in row["Possui Pacote/Seguro?"] for name in validNames) and row["Possui Pacote/Seguro?"] != "SEM PACOTE":
                    df.at[i, "Tabela Cod Desc"] = None
                    df.at[i, "Cod Produto"] = 0

            logger.info("Processamento do C6bankcomissao finalizado com sucesso")
            return df
        except Exception:
            logger.exception("Erro ao editar C6bankcomissao")
            logger.error("Erro ao editar C6bankcomissao")
            return "Erro ao editar C6bankcomissao"
        finally:
            logger.info("Finalizado processo de edicao C6bankcomissao")