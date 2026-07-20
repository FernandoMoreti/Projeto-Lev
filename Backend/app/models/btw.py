import pandas as pd
import os
from .bank import Bank
import logging
import numpy as np

logger = logging.getLogger("bancos")
class Btw(Bank):
    def __init__(self, name = "BTW BANK", num = 10501, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-Btw")
            df = pd.read_excel(df)
            logger.info("Lido o arquivo do Btw")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):
        try:
            logger.info("Iniciando processo de edicao do BTW")

            filename = df.filename

            df = self.readArchive(df)
            if isinstance(df, str):
                return df

            listOfLines = []
            type = ""

            if filename.split("_")[1] == "BTW":

                for index, row in df.iterrows():
                    if row["Vr_Seguro_Bruto"] > 0:
                        rowSeguro = row.copy()
                        rowSeguro["Vr_Serviço_Bruto"] = rowSeguro["Vr_Seguro_Bruto"]
                        rowSeguro["type"] = "SEGURO"
                        listOfLines.append(rowSeguro)

                    row["type"] = "BÔNUS"
                    listOfLines.append(row)

                df = pd.DataFrame(listOfLines)

                infos = {
                    "Proposta": "NUM_PROPOSTA",
                    "DT_Pagamento": "DAT_CREDITO",
                    "Valor_Liberado": "VAL_BASE_COMISSAO",
                    "Vr_Serviço_Bruto": "VAL_COMISSAO",
                    "type": "TIPO_COMISSAO_BANCO",
                }

            elif filename.split("_")[1] == "LECCA":

                df["type"] = "DIRETA"

                infos = {
                    "Proposta": "NUM_PROPOSTA",
                    "DT_Pagamento": "DAT_CREDITO",
                    "Valor_Operacao": "VAL_BASE_COMISSAO",
                    "Vr_Comissao_Bruto": "VAL_COMISSAO",
                    "type": "TIPO_COMISSAO_BANCO",
                }
            else:
                return "Erro: Arquivo não reconhecido"

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            for index, row in df_novo.iterrows():
                if row["VAL_COMISSAO"] < 0:
                    df_novo.at[index, "TIPO_COMISSAO_BANCO"] = "ESTORNO"

            df_novo["NUM_BANCO"] = 10501
            df_novo["NOM_BANCO"] = "BTW BANK"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100

            logger.info("Processamento do BTW finalizado com sucesso")
            return df_novo

        except Exception:
            logger.exception("Erro ao editar BTW")
            return "Erro ao editar BTW"
        finally:
            logger.info("Finalizado processo de edicao BTW")
