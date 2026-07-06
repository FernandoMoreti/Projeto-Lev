import pandas as pd
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class C6bankcomissao(Bank):
    def __init__(self, name = "C6 AUTO", num = 3336, type = "excel"):
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

            df = self.readArchive(df)

            infos = {
                "Número Proposta": "NUM_PROPOSTA",
                "Data Pagamento": "DAT_CREDITO",
                "Parcelas": "QTD_PARCELA",
                "Valor Base": "VAL_BASE_COMISSAO",
                "Perc à Vista": "PCL_COMISSAO",
                "Motivo": "DSC_OBSERVACAO",
                "Valor Bruto": "VAL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            for row in df.iterrows():
                if row[1]["Nome Comissionado"] != "LEV":
                    df.at[row[0], "Valor Bruto"] = 0

            df["Data Pagamento"] = df["Data Pagamento"].dt.strftime("%Y-%m-%d")
            df["Data Oper/ Data Inclusão"] = df["Data Oper/ Data Inclusão"].dt.strftime("%Y-%m-%d")

            logger.info("Processamento do c6bankcomissao finalizado com sucesso")
            return df
        except Exception:
            logger.exception("Erro ao editar c6bankcomissao")
            logger.error("Erro ao editar c6bankcomissao")
            return "Erro ao editar c6bankcomissao"
        finally:
            logger.info("Finalizado processo de edicao c6autocomissao")