import pandas as pd
from datetime import datetime
from ..utils import createDataframe, inputValueColumns, validDf
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Jbcred(Bank):
    def __init__(self, name = "JBCRED", num = 777, type = "html"):
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

            now = datetime.now()
            current_date = now.strftime("%d/%m/%Y")

            df = self.readArchive(df)

            infos ={
                "NRCONTRATO":"NUM_PROPOSTA",
                "VLR_OPER":"VAL_BASE_COMISSAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            num_propostas = []

            for num in df_novo["NUM_PROPOSTA"]:
                num_str = str(num)
                num_str = num_str.replace("-", "")
                num_float = float(num_str)
                num_propostas.append(num_float)

            df_novo["NUM_PROPOSTA"] = num_propostas
            df_novo["DAT_CREDITO"] = current_date
            df_novo["NOM_BANCO"] = "JBCRED"
            df_novo["PCL_COMISSAO"] = 10
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] / 10
            df_novo["NUM_BANCO"] = 777
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            logger.info("Processamento do Jbcred finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Jbcred")
            logger.error("Erro ao editar Jbcred")
            return "Erro ao editar Jbcred"
        finally:
            logger.info("Finalizado processo de edicao Jbcred")