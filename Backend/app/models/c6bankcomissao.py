import pandas as pd
import logging
from .bank import Bank
from ..mapper import COMISSAO_MAPPER

logger = logging.getLogger("bancos")

class C6bankcomissao(Bank):
    def __init__(self, name = "C6 AUTO", num = 3336, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df)
            df = df[pd.notna(df["Número Proposta"])]
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
                "Categoria": "TIPO_COMISSAO_BANCO",
                "Valor Bruto": "VAL_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            for row in df.iterrows():
                if row[1]["Nome Comissionado"] != "LEV":
                    df.at[row[0], "Valor Bruto"] = 0

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            list_types = []

            for index, row in df_novo.iterrows():
                type_row = COMISSAO_MAPPER[row["TIPO_COMISSAO_BANCO"].upper()]
                list_types.append(type_row)

            df_novo["NUM_BANCO"] = "336"
            df_novo["NOM_BANCO"] = "C6BANK"
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100
            df_novo["DAT_CREDITO"] = df_novo["DAT_CREDITO"].dt.strftime("%Y-%m-%d")
            df_novo["TIPO_COMISSAO_BANCO"] = list_types

            logger.info("Processamento do c6bankcomissao finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar c6bankcomissao")
            logger.error("Erro ao editar c6bankcomissao")
            return "Erro ao editar c6bankcomissao"
        finally:
            logger.info("Finalizado processo de edicao c6autocomissao")