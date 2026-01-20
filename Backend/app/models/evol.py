import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Evol(Bank):
    def __init__(self, name = "EVOL", num = 7777, type = "excel"):
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

            infos ={
                "Id_Operation":"NUM_PROPOSTA",
                "Taxa":"PCL_TAXA_EMPRESTIMO",
                "Valor_Liberado":"VAL_LIQUIDO",
                "Valor_Saldo":"VAL_COMISSAO",
                "Valor_Bruto":"VAL_BRUTO",
                "Data de Pagamento Comissão":"DAT_CREDITO",
                "Percentual_Comissao":"PCL_COMISSAO",
                "Descricao_Tipo_Operacao" :"DSC_TIPO_PROPOSTA_EMPRESTIMO"
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            for index, row in df_novo.iterrows():
                if row["DSC_TIPO_PROPOSTA_EMPRESTIMO"] == "PORT + REFIN - NORMAL":
                    df_novo.at[index, "VAL_BASE_COMISSAO"] = row["VAL_BRUTO"]
                else:
                    df_novo.at[index, "VAL_BASE_COMISSAO"] = row["VAL_LIQUIDO"]

            df_novo["NOM_BANCO"] = "EVOL"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["NUM_BANCO"] = 7777
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
            df_novo["DSC_TIPO_PROPOSTA_EMPRESTIMO"] = None

            logger.info("Processamento do Evol finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Evol")
            logger.error("Erro ao editar Evol")
            return "Erro ao editar Evol"
        finally:
            logger.info("Finalizado processo de edicao Evol")