import pandas as pd
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class C6bankcreditomanual(Bank):
    def __init__(self, name = "C6 BANK CREDITO MANUAL", num = 0, type = "excel"):  # num não especificado, coloquei 0
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
            logger.info("Iniciando processo de edicao do C6bankcreditomanual")

            df = self.readArchive(df)
            if isinstance(df, str):
                return df

            validNames = ["DEVOLUÇÃO", "DEVOLUCAO"]

            for i, row in df.iterrows():
                motivo = str(row["Motivo"]).upper()
                if any(name in motivo for name in validNames) and row["Categoria"] == "REFIN PORT-PGTO COMISSAO FLAT":
                    df.at[i, "Categoria"] = (f"{row['Categoria']}  reembolso")

                if row["Loja Recebedora"] != "LEV":
                    df.at[i, "Valor Estorno"] = 0
                    df.at[i, "Valor Total"] = 0
                    df.at[i, "Perc À Vista"] = 0
                    df.at[i, "Cod Master Imediato"] = 0

            df = df.drop(columns=["Valor Bruto Refin Portabilidade"])

            df["Valor Crédito"] = df["Valor Crédito"].astype(float)
            df["Valor Estorno"] = df["Valor Estorno"].astype(float)
            df["Valor Total"] = df["Valor Total"].astype(float)
            df["Valor Estorno"] = df["Valor Total"]
            df["Valor Base"] = df["Valor Base"].astype(float)
            df["Valor Financiado"] = df["Valor Financiado"].astype(float)
            df["Valor Líquido Crédito"] = df["Valor Líquido Crédito"].astype(float)

            logger.info("Processamento do C6bankcreditomanual finalizado com sucesso")
            return df
        except Exception:
            logger.exception("Erro ao editar C6bankcreditomanual")
            logger.error("Erro ao editar C6bankcreditomanual")
            return "Erro ao editar C6bankcreditomanual"
        finally:
            logger.info("Finalizado processo de edicao C6bankcreditomanual")