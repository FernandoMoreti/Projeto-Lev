import pandas as pd
from datetime import timedelta
from ..utils import convertValues
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Crefisa(Bank):
    def __init__(self, name = "BANCO CREFISA S.A.", num = 69, type = "html"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_html(df, header=0)[0]
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
               "Num_Proposta":"NUM_PROPOSTA",
               "Data_Geracao_Comissao":"DAT_CREDITO",
               "Vlr_Liquido":"VAL_BASE_COMISSAO",
               "Vlr_Pagamento_Comissao":"VAL_COMISSAO",
               "Perc_Pagamento_Comissao":"PCL_COMISSAO",
               "Tipo":"TIPO_COMISSAO_BANCO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            for index, row in df_novo.iterrows():
                if row["TIPO_COMISSAO_BANCO"] == "À Vista":
                    df_novo.at[index, "TIPO_COMISSAO_BANCO"] = "DIRETA"

            print(df_novo["VAL_COMISSAO"])
            print(df_novo["VAL_BASE_COMISSAO"])

            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")
            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")

            df_novo["NUM_BANCO"] = 69
            df_novo["NOM_BANCO"] = 'BANCO CREFISA S.A.'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]


            logger.info("Processamento do Crefisa finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Crefisa")
            logger.error("Erro ao editar Crefisa")
            return "Erro ao editar Crefisa"
        finally:
            logger.info("Finalizado processo de edicao Crefisa")