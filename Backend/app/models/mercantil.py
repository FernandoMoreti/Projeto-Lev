import pandas as pd
from ..utils import validDf, convertValues
import logging
from .bank import Bank
from ..mapper import MERCANTIL

logger = logging.getLogger("bancos")

class Mercantil(Bank):
    def __init__(self, name = "MERCANTIL", num = 389, type = "csv"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-Mercantil")
            df = pd.read_csv(df, sep=";")
            df = df.iloc[:-1]

            df["IDENTIFICADOR"] = df["IDENTIFICADOR"].astype(str).str.strip().str.lstrip("0")

            logger.info("Lido o arquivo do Mercantil")
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
                "IDENTIFICADOR": "NUM_PROPOSTA",
                "VLR BASE OPERACAO": "VAL_BASE_COMISSAO",
                "VLR COMISSAO CON": "VAL_COMISSAO",
                "PERIODO FIM PAGTO": "DAT_CREDITO",
                "TIPO PAGAMENTO": "TIPO_COMISSAO_BANCO"
            }

            logger.info("Validando dataframe")

            Error = validDf(df, infos)
            if Error:
                return Error

            logger.info("Dataframe validado")
            logger.info("Criando Dataframe")

            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            logger.info("Dataframe criado com sucesso")

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, 'VAL_BASE_COMISSAO')
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, 'VAL_COMISSAO')

            logger.info("Adicionando valores de forma fixa")

            df_novo["NUM_BANCO"] = '389'
            df_novo["NOM_BANCO"] = 'BANCO MERCANTIL DO BRASIL'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100

            listTypes = []

            for index, row in df_novo.iterrows():
                print(row["TIPO_COMISSAO_BANCO"])
                listTypes.append(MERCANTIL[row["TIPO_COMISSAO_BANCO"].strip()])

            df_novo["TIPO_COMISSAO_BANCO"] = listTypes

            return df_novo
        except:
            logger.exception("Erro ao editar Mercantil")
            logger.error("Erro ao editar Mercantil")
            return "Erro ao editar Mercantil"
        finally:
            logger.info("Finalizado processo de edicao Mercantil")