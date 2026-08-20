import pandas as pd
from ..utils import convertValues
from .bank import Bank
import logging
from ..mapper import BMG

logger = logging.getLogger("bancos")

class BmgRotativo(Bank):
    def __init__(self, name = "BMG", num = 701, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-BMG Rotativo")
            df = pd.read_csv(df, sep=';', encoding='latin-1')
            logger.info("Lido o arquivo do BMG Rotativo")
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

            if "Comissão Ato ou Diferido" in df.columns:
                infos ={
                    "Adesao":"NUM_PROPOSTA",
                    "Valor Base": "VAL_BASE_COMISSAO",
                    "Valor Bruto": "VAL_COMISSAO",
                    "Data Pagamento": "DAT_CREDITO",
                    "Comissão Ato ou Diferido": "TIPO_COMISSAO_BANCO",
                }
            else:
                infos ={
                    "Adesao":"NUM_PROPOSTA",
                    "Valor Base": "VAL_BASE_COMISSAO",
                    "Valor Bruto": "VAL_COMISSAO",
                    "Data Pagamento": "DAT_CREDITO",
                    "Tipo de Comissao": "TIPO_COMISSAO_BANCO",
                    "% de Comissao": "PCL_COMISSAO",
                }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()

            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")

            df_novo["NUM_BANCO"] = 318
            df_novo["NOM_BANCO"] = 'BANCO BMG S.A.'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100

            list_types = []

            if "Comissão Ato ou Diferido" in df.columns:
                for index, row in df_novo.iterrows():
                    if row["TIPO_COMISSAO_BANCO"] == "Diferido":
                        list_types.append("DIFERIDA")
                    else:
                        list_types.append("DIRETA")
            else:
                for index, row in df_novo.iterrows():
                    type_row = BMG[row["TIPO_COMISSAO_BANCO"].upper()]
                    if type_row == ["DIRETA", "DIFERIDA"]:
                        if pd.notna(row["PCL_COMISSAO"]):
                            if row["PCL_COMISSAO"] == 100:
                                list_types.append("PRÉ-ADESÃO")
                            else:
                                list_types.append("DIRETA")
                        else:
                            list_types.append("DIFERIDA")
                    else:
                        list_types.append(type_row)

            df_novo["TIPO_COMISSAO_BANCO"] = list_types

            return df_novo
        except Exception:
            logger.exception("Erro ao editar Bmg")
            logger.error("Erro ao editar Bmg")
            return "Erro ao editar Bmg"
        finally:
            logger.info("Finalizado processo de edicao Bmg")