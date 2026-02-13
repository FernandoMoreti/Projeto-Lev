import pandas as pd
import requests
from ..utils import convertValues
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Facta(Bank):
    def __init__(self, name = "FACTA", num = 0, type = "excel"):  # num não especificado, coloquei 0
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df, engine="openpyxl")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do Facta")

            df = self.readArchive(df)
            if isinstance(df, str):
                return df

            session = requests.Session()
            bruto_por_proposta = {}
            list_props = []

            for idx in df.index:
                obs = str(df.at[idx, "OBSERVACAO"])
                proposta = df.at[idx, "CODIGOAF"]

                list_props.append(proposta)
                if "PGTO ADIANTAMENTO" in obs and proposta not in bruto_por_proposta:
                    try:
                        response = session.get(
                            f"http://192.168.1.252:3004/v1/wb-api/proposta/?proposal={proposta}",
                            timeout=10
                        )
                        data = response.json()

                        if data[0]["tipo"] == "PORTAB/REFIN":
                            bruto_por_proposta[proposta] = data[0]["bruto"]

                    except Exception as e:
                        logger.error(f"Erro proposta {proposta}: {e}")

                if "Desconto IR" in obs:
                    df.drop(idx, inplace=True)

            df["VLRAF"] = df["CODIGOAF"].map(bruto_por_proposta).fillna(df["VLRAF"])

            df["VLRAF"] = convertValues(df, "VLRAF")

            logger.info("Processamento do Facta finalizado com sucesso")
            return df
        except Exception:
            logger.exception("Erro ao editar Facta")
            logger.error("Erro ao editar Facta")
            return "Erro ao editar Facta"
        finally:
            logger.info("Finalizado processo de edicao Facta")