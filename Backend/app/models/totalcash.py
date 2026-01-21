import pandas as pd
import logging
from datetime import datetime
from ..utils import convertValues
import requests
from .bank import Bank

logger = logging.getLogger("bancos")

class Totalcash(Bank):
    def __init__(self, name = "TOTALCASH", num = 1731, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df, usecols=[
                    "Nr Proposta",
                    "Valor Liberado Cliente",
                    "Valor Comissão",
                    "Taxa Pagamento"
                ])
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do Totalcash")

            df = self.readArchive(df)

            infos = {
                "Nr Proposta": "NUM_PROPOSTA",
                "Valor Liberado Cliente": "VAL_BASE_COMISSAO",
                "Valor Comissão": "VAL_COMISSAO",
                "Taxa Pagamento": "PCL_TAXA_EMPRESTIMO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            del df

            mask_estorno = df_novo["VAL_COMISSAO"] < 0

            df_novo.loc[~mask_estorno, "TIPO_COMISSAO_BANCO"] = "DIRETA"

            session = requests.Session()

            for idx in df_novo.index:
                val_comissao = df_novo.at[idx, "VAL_COMISSAO"]

                proposta = df_novo.at[idx, "NUM_PROPOSTA"]

                try:
                    response = session.get(
                        f"http://192.168.1.252:3004/v1/wb-api/proposta/?proposal={proposta}",
                        timeout=5
                    )

                    response.raise_for_status()

                    data = response.json()

                    if val_comissao < 0:
                            df_novo.at[idx, "VAL_BASE_COMISSAO"] = data[0]["bruto"]
                            df_novo.at[idx, "TIPO_COMISSAO_BANCO"] = "ESTORNO"

                    else:
                        if data[0]["tipo"] == "PORTAB/REFIN":
                            df_novo.at[idx, "VAL_BASE_COMISSAO"] = data[0]["bruto"]

                        df_novo.at[idx, "TIPO_COMISSAO_BANCO"] = "DIRETA"


                except Exception as e:
                    df_novo.at[idx, "TIPO_COMISSAO_BANCO"] = "ERRO_API"
                    print(f"Erro proposta {proposta}: {e}")


            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")

            df_novo["NUM_BANCO"] = 1731
            df_novo["NOM_BANCO"] = "TOTALCASH"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["DAT_CREDITO"] = datetime.now().date()
            df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100

            logger.info("Processamento do Totalcash finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Totalcash")
            logger.error("Erro ao editar Totalcash")
            return "Erro ao editar Totalcash"
        finally:
            logger.info("Finalizado processo de edicao Totalcash")