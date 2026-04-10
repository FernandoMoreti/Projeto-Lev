import pandas as pd
import camelot
from PyPDF2 import PdfReader
from ..utils import convertValues, paintLine
from .bank import Bank
import logging
from datetime import datetime

logger = logging.getLogger("bancos")

class Brbinconta(Bank):
    def __init__(self, name = "BRB - BANCO DE BRASÍLIA", num = 70, type = "pdf"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-BRBInconta")
            tables = camelot.read_pdf(df, pages='all',flavor="stream")

            reader = PdfReader(df)
            pages = len(reader.pages)

            if not tables:
                logger.error("Nenhuma tabela encontrada no pdf")
                return "Nenhuma tabela encontrada no PDF"

            isBigger = False

            if pages < 3:
                for index, table in enumerate(tables):
                    if index == 1:
                        if len(table.df.columns) > 5:
                            table.df = table.df.drop(columns=[1])
                            table.df = table.df.drop(columns=[2])
                            table.df = table.df.drop(columns=[5])
                        table.df.columns = range(table.df.shape[1])
                    if len(table.df[0]) > 45:
                        table.df = table.df.drop(columns=[1])
                        table.df.columns = range(table.df.shape[1])
                        isBigger = True
                    else:
                        if isBigger or index == 1:
                            table.df = table.df.iloc[2:]
                        else:
                            table.df = table.df.iloc[6:]

            if pages == 3:
                for index, table in enumerate(tables):
                    if index == 1 or index == 2:
                        pass
                    else:
                        if len(table.df.columns) > 9:
                            table.df = table.df.drop(columns=[1])
                            table.df.columns = range(table.df.shape[1])

            if pages > 3:
                for index, table in enumerate(tables):
                    if index == 1:
                        table.df = table.df.drop(columns=[1])
                        table.df.columns = range(table.df.shape[1])

            df = pd.concat([table.df for table in tables], ignore_index=True)

            df = df.replace(r'^\s*$', pd.NA, regex=True)

            df = df.dropna(thresh=8) # remove linhas que tenham pelo menos 10 colunas preenchidas

            if len(df.columns) > 8:
                df = df.drop(columns=[1])
                df.columns = range(df.shape[1])

            df[4] = df[4].replace(pd.NA, 0)

            if pages > 2:
                df = df.iloc[:-1]
                df = df.iloc[1:]

            logger.info("Lido o arquivo do BRBInconta")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.erro("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
           logger.info("Finalizando processo de leitura do arquivo")


    def run(self, df):

        try:
            logger.info("Iniciando processo de edicao do BrbInconta")

            df = self.readArchive(df)
            date = datetime.now().strftime("%d/%m/%Y")

            infos = {
                1 : "NUM_PROPOSTA",
                2 : "DSC_OBSERVACAO",
                3 : "QTD_PARCELA",
                4 : "PCL_COMISSAO",
                6 : "VAL_BASE_COMISSAO",
                7 : "VAL_COMISSAO",
            }

            logger.info("Iniciando processo de edicao do BTW")

            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Iniciando processo de edicao do BTW")
            logger.info("Iniciando processo de edicao do BTW")

            df_novo = self.createDataframe()

            df_novo = self.inputValues(df, df_novo, infos)

            logger.info("Iniciando processo de edicao do BTW")
            logger.info("Iniciando processo de edicao do BTW")

            df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
            df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")

            valores_tratados = []

            for valor in df_novo["DSC_OBSERVACAO"]:

                print(valor)

                valor_str = valor

                if type(valor) == str :

                    valor_str = str(valor)

                    valor_teste = valor_str.replace("%", "")
                    valor_teste = valor_teste.strip()
                    if valor_teste.split(" ")[-1] == "MARGEM":
                        valor_teste = valor_teste.split(" ")[-2].replace("/", "")
                    else:
                        valor_teste = valor_teste.split(" ")[-1]
                    valor_teste = valor_teste.replace(",", ".")
                    if valor_teste == "SAQUE":
                        valor_teste = "0"
                    if valor == "CONTA":
                        valores_tratados.append(0.0)
                        continue
                    valor_str = float(valor_teste)

                valores_tratados.append(valor_str)

            df_novo["PCL_TAXA_EMPRESTIMO"] = valores_tratados

            logger.info("Iniciando processo de edicao do BTW")

            print(df_novo["PCL_COMISSAO"])

            df_novo["PCL_COMISSAO"] = pd.to_numeric(df_novo["PCL_COMISSAO"].astype(str).str.replace(",", "."), errors='coerce').fillna(0)
            df_novo["NUM_PROPOSTA"] = pd.to_numeric(df_novo["NUM_PROPOSTA"], errors='coerce').fillna(0).astype('int64')
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["NUM_BANCO"] = 70
            df_novo["NOM_BANCO"] = 'BRB - BANCO DE BRASÍLIA'
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
            df_novo["DSC_OBSERVACAO"] = None
            df_novo["DAT_CREDITO"] = date

            df_novo = df_novo.style.apply(paintLine, axis=1)

            return df_novo
        except Exception:
            logger.exception("Erro ao editar BrbInconta")
            logger.error("Erro ao editar BrbInconta")
            return "Erro ao editar BrbInconta"
        finally:
            logger.info("Finalizado processo de edicao BrbInconta")