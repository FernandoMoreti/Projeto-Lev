import pandas as pd
import os
from .bank import Bank
import logging

logger = logging.getLogger("bancos")
class Btw(Bank):
    def __init__(self, name = "BTW BANK", num = 10501, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-Btw")
            df = pd.read_excel(df)
            logger.info("Lido o arquivo do Btw")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")


    def findArchive(self, df):
        try:
            logger.info("Iniciando busca por arquivo relacionado no BTW")
            numMes = (df.filename.split('_')[2].split('-')[0][4:6])
            mes = self.meses((df.filename.split('_')[2].split('-')[0][4:6]))
            ano = (df.filename.split('_')[2].split('-')[0][0:4])

            if df.filename.split('_')[1] == "BTW":
                name = "LECCA"
            else:
                name = "BTW"

            data = f"{name}_{df.filename.split('_')[2]}"

            caminho_pasta = f"Z:\COMISSÃO\DOCS - WORK BANK {ano}\BTW\\{numMes} - {mes}"
            arquivos = os.listdir(caminho_pasta)

            arquivo_encontrado = None

            for arquivo in arquivos:
                if data in arquivo:
                    arquivo_encontrado = arquivo
                    break

            if arquivo_encontrado:
                caminho_completo = os.path.join(caminho_pasta, arquivo_encontrado)
                df_encontrado = pd.read_excel(caminho_completo)
                logger.info(f"Arquivo relacionado encontrado: {arquivo_encontrado}")
                return df_encontrado, name
            else:
                logger.error(f"Arquivo não encontrado para a data: {data}")
                return "Arquivo não encontrado para a data:", None
        except Exception as e:
            logger.exception("Erro ao buscar arquivo relacionado")
            return f"Erro ao buscar arquivo: {str(e)}", None
        finally:
            logger.info("Finalizando busca por arquivo relacionado")

    def renameColumns(self, df_encontrado, df, name):
        print(df)
        try:
            logger.info(f"Renomeando colunas para {name}")
            if name == "LECCA":
                df_encontrado.rename(columns={
                    "Vr_Comissao_Flat_Bruto" : "Total_Bruto",
                    "Tx_Comissao_Flat" : "Tx_Serviço"
                }, inplace=True)
                df_encontrado['tipo'] = 'DIRETA'
                df['tipo'] = 'BÔNUS'
            else:
                df_encontrado.rename(columns={
                    "Total_Bruto" : "Vr_Comissao_Flat_Bruto",
                    "Tx_Serviço" : "Tx_Comissao_Flat",
                }, inplace=True)
                df_encontrado['tipo'] = 'BÔNUS'
                df['tipo'] = 'DIRETA'
            logger.info("Colunas renomeadas com sucesso")
            return df_encontrado, df
        except Exception:
            logger.exception("Erro ao renomear colunas")
            return df_encontrado, df


    def meses(self, mes):

        meses= {
            "01": "JANEIRO",
            "02": "FEVEREIRO",
            "03": "MARÇO",
            "04": "ABRIL",
            "05": "MAIO",
            "06": "JUNHO",
            "07": "JULHO",
            "08": "AGOSTO",
            "09": "SETEMBRO",
            "10": "OUTUBRO",
            "11": "NOVEMBRO",
            "12": "DEZEMBRO"
        }

        return meses.get(mes, "Mês inválido")

    def run(self, df):
        try:
            logger.info("Iniciando processamento do BTW")

            df_encontrado, name = self.findArchive(df)

            df = self.readArchive(df)

            df_encontrado, df = self.renameColumns(df_encontrado, df, name)

            df = pd.concat([df_encontrado, df], ignore_index=True)
            logger.info("DataFrames concatenados")

            if name == "LECCA":
                infos = {
                    "Proposta": "NUM_PROPOSTA",
                    "DT_Pagamento": "DAT_CREDITO",
                    "Valor_Liberado": "VAL_BASE_COMISSAO",
                    "Total_Bruto": "VAL_COMISSAO",
                    "Tx_Serviço": "PCL_COMISSAO",
                    "tipo": "TIPO_COMISSAO_BANCO",
                }
            else:
                infos = {
                    "Proposta": "NUM_PROPOSTA",
                    "DT_Pagamento": "DAT_CREDITO",
                    "Valor_Liberado": "VAL_BASE_COMISSAO",
                    "Vr_Comissao_Flat_Bruto": "VAL_COMISSAO",
                    "Tx_Comissao_Flat": "PCL_COMISSAO",
                    "tipo": "TIPO_COMISSAO_BANCO",
                }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()

            df_novo = self.inputValues(df, df_novo, infos)

            df_novo["NUM_BANCO"] = 10501
            df_novo["NOM_BANCO"] = "BTW BANK"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100

            logger.info("Processamento do BTW finalizado com sucesso")
            return df_novo
        except Exception as e:
            logger.exception("Erro no processamento do BTW")
            return f"Erro no processamento: {str(e)}"