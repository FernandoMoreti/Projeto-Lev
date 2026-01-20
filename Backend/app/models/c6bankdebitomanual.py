import pandas as pd
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class C6bankdebitomanual(Bank):
    def __init__(self, name = "C6 BANK DEBITO MANUAL", num = 0, type = "excel"):  # num não especificado, coloquei 0
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
            logger.info("Iniciando processo de edicao do C6bankdebitomanual")

            df = self.readArchive(df)
            if isinstance(df, str):
                return df

            listMotivo = {
                "Estorno - Pag Duplicado - Comissao Port": "EST DUPLICIDADE EST PGTO COMISSAO FLAT",
                "Estorno - Pagamento de Complemento de TC e Seguro - Manual Indevido": "ESTORNO TAXA",
                "Estorno - Devolucao de pendencia FÝsico - ComissÒo ficou a maior": "AJUSTE DE PAGAMENTO A MAIOR",
                "Ajuste de Pagamento A Maior": "Ajuste de Pagamento A Maior",
            }

            for i, row in df.iterrows():
                if row["Loja Recebedora"] != "LEV":
                    df.at[i, "Valor Total"] = 0

            for i, motivo in listMotivo.items():
                if row["Motivo"] == motivo:
                    df.at[i, "Categoria"] = listMotivo[row["Motivo"]]
                    df.at[i, "Situação"] = listMotivo[row["Motivo"]]

            df["Valor Débito"] = df["Valor Débito"].astype(float)
            df["Valor Estorno"] = df["Valor Estorno"].astype(float)
            df["Valor Total"] = df["Valor Total"].astype(float)

            logger.info("Processamento do C6bankdebitomanual finalizado com sucesso")
            return df
        except Exception:
            logger.exception("Erro ao editar C6bankdebitomanual")
            logger.error("Erro ao editar C6bankdebitomanual")
            return "Erro ao editar C6bankdebitomanual"
        finally:
            logger.info("Finalizado processo de edicao C6bankdebitomanual")