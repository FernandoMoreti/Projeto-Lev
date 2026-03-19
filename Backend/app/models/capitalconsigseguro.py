import pandas as pd
import logging
from datetime import datetime
from .bank import Bank

logger = logging.getLogger("bancos")

class CapitalConsigSeguro(Bank):
    def __init__(self, name = "QUERO MAIS CREDITO", num = 3030, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df, header=4)
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do Queromaisseguro")

            df = self.readArchive(df)

            infos = {
               "Contrato":"NUM_PROPOSTA",
               "VALOR DE SEGURO":"VAL_BASE_COMISSAO",
               "OBS":"DSC_OBSERVACAO",
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            for row in df_novo.itertuples():
                print(row.DSC_OBSERVACAO)
                if pd.isna(row.DSC_OBSERVACAO):
                    df_novo.at[row.Index, "TIPO_COMISSAO_BANCO"] = 'SEGURO'
                else:
                    df_novo.at[row.Index, "TIPO_COMISSAO_BANCO"] = 'ESTORNO SEGURO'

            df_novo["NUM_BANCO"] = 3030
            df_novo["NOM_BANCO"] = 'QUERO MAIS CREDITO'
            df_novo["DAT_CREDITO"] = datetime.now().date()
            df_novo["PCL_COMISSAO"] = 30
            df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] * 0.3
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            logger.info("Processamento do Queromaisseguro finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Queromaisseguro")
            logger.error("Erro ao editar Queromaisseguro")
            return "Erro ao editar Queromaisseguro"
        finally:
            logger.info("Finalizado processo de edicao Queromaisseguro")