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
                name = "BTW"
            else:
                name = "LECCA"

            data = f"{name}_{df.filename.split('_')[2]}"

            caminho_pasta = f"Z:\COMISSÃO\DOCS - WORK BANK {ano}\BTW\\{numMes} - {mes}"
            arquivos = os.listdir(caminho_pasta)

            if not os.path.exists(caminho_pasta):
                logger.warning(f"Pasta não encontrada: {caminho_pasta}")
                return None, name

            arquivo_encontrado = None
            arquivos = os.listdir(caminho_pasta)

            for arquivo in arquivos:
                if data in arquivo:
                    arquivo_encontrado = arquivo
                    break

            if not arquivo_encontrado:
                logger.info("Nenhum arquivo relacionado encontrado.")
                return None, name

            caminho_completo = os.path.join(caminho_pasta, arquivo_encontrado)
            df_encontrado = pd.read_excel(caminho_completo)

            logger.info(f"Arquivo relacionado encontrado: {arquivo_encontrado}")
            return df_encontrado, name
        except Exception as e:
            logger.exception("Erro ao buscar arquivo relacionado")
            return f"Erro ao buscar arquivo: {str(e)}", None
        finally:
            logger.info("Finalizando busca por arquivo relacionado")

    def renameColumns(self, df_encontrado, df, name):
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
            logger.info("Iniciando processo de edicao do BTW")

            unique = False

            df_encontrado, related_name = self.findArchive(df)

            df_main = self.readArchive(df)
            if isinstance(df_main, str):
                return df_main

            if df_encontrado is not None:
                df_encontrado, df_main = self.renameColumns(df_encontrado, df_main, related_name)
                df_final = pd.concat([df_encontrado, df_main], ignore_index=True)

                if related_name == "LECCA":
                    infos = {
                        "Proposta": "NUM_PROPOSTA",
                        "DT_Pagamento": "DAT_CREDITO",
                        "Valor_Liberado": "VAL_BASE_COMISSAO",
                        "Vr_Comissao_Bruto": "VAL_COMISSAO",
                        "Tx_Comissao": "PCL_COMISSAO",
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

            else:

                df_final = df_main
                unique = True

                if related_name == "LECCA":
                    infos = {
                        "Proposta": "NUM_PROPOSTA",
                        "DT_Pagamento": "DAT_CREDITO",
                        "Valor_Liberado": "VAL_BASE_COMISSAO",
                        "Vr_Comissao_Bruto": "VAL_COMISSAO",
                        "Tx_Comissao": "PCL_COMISSAO",
                    }
                else:
                    infos = {
                        "Proposta": "NUM_PROPOSTA",
                        "DT_Pagamento": "DAT_CREDITO",
                        "Valor_Liberado": "VAL_BASE_COMISSAO",
                        "Total_Bruto": "VAL_COMISSAO",
                    }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df_final, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df_final, df_novo, infos)

            if unique:
                df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

            df_novo["NUM_BANCO"] = 10501
            df_novo["NOM_BANCO"] = "BTW BANK"
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            if related_name == "LECCA":
                df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100
            else:
                df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100


            logger.info("Processamento do BTW finalizado com sucesso")
            return df_novo

        except Exception:
            logger.exception("Erro ao editar BTW")
            return "Erro ao editar BTW"
        finally:
            logger.info("Finalizado processo de edicao BTW")
