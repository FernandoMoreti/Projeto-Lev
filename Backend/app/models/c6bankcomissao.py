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

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            for row in df.iterrows():
                if row[1]["Nome Comissionado"] != "LEV":
                    df_novo.at[row[0], "VAL_COMISSAO"] = 0

                if row[1]["Débito/Crédito"] == "D":
                    if row[1]["Motivo"].split(" ")[1] == "SEGURO":
                        df_novo.at[row[0], "TIPO_COMISSAO_BANCO"] = "ESTORNO SEGURO"
                    elif row[1]["Motivo"].split(" ")[2] == "PACOTE":
                        df_novo.at[row[0], "TIPO_COMISSAO_BANCO"] = "ESTORNO PACOTE BENEFICIO"
                    else:
                        df_novo.at[row[0], "TIPO_COMISSAO_BANCO"] = "ESTORNO"

                if row[1]["Débito/Crédito"] == "C":
                    if row[1]["Motivo"].split(" ")[1] == "SEGURO":
                        df_novo.at[row[0], "TIPO_COMISSAO_BANCO"] = "SEGURO"
                    elif row[1]["Motivo"].split(" ")[2] == "PACOTE":
                        df_novo.at[row[0], "TIPO_COMISSAO_BANCO"] = "PACOTE BENEFICIO"
                    else:
                        df_novo.at[row[0], "TIPO_COMISSAO_BANCO"] = "DIRETA"

            df_novo["NUM_BANCO"] = 3336
            df_novo["NOM_BANCO"] = 'C6 AUTO'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100

            logger.info("Processamento do c6bankcomissao finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar c6bankcomissao")
            logger.error("Erro ao editar c6bankcomissao")
            return "Erro ao editar c6bankcomissao"
        finally:
            logger.info("Finalizado processo de edicao c6autocomissao")