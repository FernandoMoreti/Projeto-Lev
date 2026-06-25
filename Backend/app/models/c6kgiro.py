import pandas as pd
import logging

from ..mapper import COMISSAO_MAPPER
from .bank import Bank

logger = logging.getLogger("bancos")

class C6kgiro(Bank):
    def __init__(self, name = "C6 Kgiro", num = 3336, type = "excel"):
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
                "Proposta Consignado": "NUM_PROPOSTA",
                "Data Pagamento Kgiro": "DAT_CREDITO",
                "Valor Contrato Consignado": "VAL_BASE_COMISSAO",
                "Valor Kgiro": "VAL_COMISSAO",
                "Tipo Antecipação Detalhe": "DSC_TIPO_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            list_types = []

            for index, row in df_novo.iterrows():
                type_row = COMISSAO_MAPPER[row["DSC_TIPO_COMISSAO"].upper()]
                list_types.append(type_row)

            df_novo["NUM_BANCO"] = 12222222
            df_novo["NOM_BANCO"] = 'C6 KGIRO'
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BRUTO"]
            df_novo["PCL_COMISSAO"] = df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"] * 100
            df_novo["TIPO_COMISSAO_BANCO"] = list_types
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            logger.info("Processamento do C6KGIRO finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar C6KGIRO")
            logger.error("Erro ao editar C6KGIRO")
            return "Erro ao editar C6KGIRO"
        finally:
            logger.info("Finalizado processo de edicao C6KGIRO")