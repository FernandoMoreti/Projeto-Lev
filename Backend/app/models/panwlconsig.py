import pandas as pd
from ..utils import convertValues
from .bank import Bank
import logging
import numpy as np
from datetime import datetime

logger = logging.getLogger("bancos")

class PanConsig(Bank):
    def __init__(self, name = "PANWL", num = 701, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-PanWl")
            df = pd.read_csv(df, sep=";", on_bad_lines='skip', header=12)
            logger.info("Lido o arquivo do PanWl")
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

            df['is_estorno'] = False

            indices_estorno = df[df.apply(lambda row: row.astype(str).str.contains("2 - Estornos de comissao").any(), axis=1)].index

            for i in range(0, len(indices_estorno), 2):
                if i + 1 < len(indices_estorno):
                    inicio = indices_estorno[i]
                    fim = indices_estorno[i+1]
                    df.loc[inicio:fim, 'is_estorno'] = True

            df = df[pd.notna(df["Valor base para calculo da comissao"])]
            df = df[df["Proposta"] != "Proposta"]
            df = df[pd.notna(df["Data Credito Comissao"])]

            infos ={
                "is_estorno": "TIPO_COMISSAO_BANCO",
                "Proposta": "NUM_PROPOSTA",
                "Valor base para calculo da comissao": "VAL_BASE_COMISSAO",
                "Valor da Comissao": "VAL_COMISSAO",
            }

            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            df_novo = self.createDataframe()

            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")

            df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
            df_novo["NUM_BANCO"] = 623
            df_novo["NOM_BANCO"] = 'PAN'
            df_novo["DAT_CREDITO"] = datetime.now().strftime("%Y-%m-%d")
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            base_comissao = df_novo["VAL_BASE_COMISSAO"]
            pcl_calculada = np.where(
                (base_comissao == 0) | (base_comissao.isna()), 
                0,
                (df_novo["VAL_COMISSAO"] / base_comissao) * 100
            )
            df_novo["PCL_COMISSAO"] = np.nan_to_num(pcl_calculada, nan=0.0)

            listOfPCL = []
            list_types = []

            for index, row in df_novo.iterrows():

                if row["TIPO_COMISSAO_BANCO"] == False:
                    list_types.append('DIRETA')
                else:
                    list_types.append('ESTORNO')

            df_novo["TIPO_COMISSAO_BANCO"] = list_types

            df_novo = df_novo.replace([np.inf, -np.inf], np.nan)
            df_novo = df_novo.where(pd.notnull(df_novo), None)

            return df_novo
        except Exception:
            logger.exception("Erro ao editar PanWl")
            logger.error("Erro ao editar PanWl")
            return "Erro ao editar PanWl"
        finally:
            logger.info("Finalizado processo de edicao PanWl")