import pandas as pd
import logging
from .bank import Bank
from ..utils import convertValues

logger = logging.getLogger("bancos")

class Santanderfvevi(Bank):
    def __init__(self, name = "SANTANDER", num = 351, type = "csv"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_csv(df, sep=";")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do Santanderfvevi")

            df = self.readArchive(df)

            infos = {
                "Proposta": "NUM_PROPOSTA",
                "Valor Bruto": "VAL_BASE_COMISSAO",
                "Valor Líquido": "VAL_LIQUIDO",
                "Percentual Comissão": "PCL_COMISSAO",
                "Valor A Vista": "VAL_COMISSAO",
                "Data do Cálculo": "DAT_CREDITO",
                "Autorregulação": "DSC_OBSERVACAO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            for idx, row in df.iterrows():
                if row["Modalidade"] == "Refinanciamento":
                    df_novo.loc[idx, "VAL_BASE_COMISSAO"] = row["Valor Líquido"]

            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_BRUTO"] = convertValues(df_novo, "VAL_BRUTO")
            df_novo["VAL_LIQUIDO"] = convertValues(df_novo, "VAL_LIQUIDO")
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100
            df_novo["NUM_BANCO"] = 351
            df_novo["NOM_BANCO"] = "SANTANDER"
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Santanderfvevi finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Santanderfvevi")
            logger.error("Erro ao editar Santanderfvevi")
            return "Erro ao editar Santanderfvevi"
        finally:
            logger.info("Finalizado processo de edicao Santanderfvevi")