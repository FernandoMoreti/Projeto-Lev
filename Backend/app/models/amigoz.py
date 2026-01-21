import pandas as pd
from ..utils import validDf
import logging
from .bank import Bank

logger = logging.getLogger("bancos")

class Amigoz(Bank):
    def __init__(self, name = "AMIGOZ", num = 7996, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            logger.info("Inicio do processo de leitura do df-Amigoz")
            df = pd.read_excel(df)
            logger.info("Lido o arquivo do Amigoz")
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.erro("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def expandir_linhas(self, row_original, row_mapeada):
        novas_linhas = []

        # Criar linha seguro
        if row_original.get("Seguro") == "Super diamante" or row_original.get("Seguro") == "Super Diamante":
            nova_linha = row_mapeada.copy()
            if row_original["Valor Seguro"] < 0:
                nova_linha["TIPO_COMISSAO_BANCO"] ="ESTORNO SEGURO"
            else:
                nova_linha["TIPO_COMISSAO_BANCO"] ="SEGURO SUPER DIAMANTE"
            nova_linha["VAL_COMISSAO"] = row_original["Valor Seguro"]
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Proposta"]
            nova_linha["PCL_COMISSAO"] = row_original["% Seguro"]
            novas_linhas.append(nova_linha)

        # Criar linha seguro
        if row_original.get("Seguro") == "Diamante":
            nova_linha = row_mapeada.copy()
            if row_original["Valor Seguro"] < 0:
                nova_linha["TIPO_COMISSAO_BANCO"] ="ESTORNO SEGURO"
            else:
                nova_linha["TIPO_COMISSAO_BANCO"] ="SEGURO DIAMANTE"
            nova_linha["VAL_COMISSAO"] = row_original["Valor Seguro"]
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Proposta"]
            nova_linha["PCL_COMISSAO"] = row_original["% Seguro"]
            novas_linhas.append(nova_linha)

        # Criar linha seguro
        if row_original.get("Seguro") == "Ouro":
            nova_linha = row_mapeada.copy()
            if row_original["Valor Seguro"] < 0:
                nova_linha["TIPO_COMISSAO_BANCO"] ="ESTORNO SEGURO"
            else:
                nova_linha["TIPO_COMISSAO_BANCO"] ="SEGURO OURO"
            nova_linha["VAL_COMISSAO"] = row_original["Valor Seguro"]
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Proposta"]
            nova_linha["PCL_COMISSAO"] = row_original["% Seguro"]
            novas_linhas.append(nova_linha)

        # Criar linha seguro
        if row_original.get("Seguro") == "Prata":
            nova_linha = row_mapeada.copy()
            if row_original["Valor Seguro"] < 0:
                nova_linha["TIPO_COMISSAO_BANCO"] ="ESTORNO SEGURO"
            else:
                nova_linha["TIPO_COMISSAO_BANCO"] ="SEGURO PRATA"
            nova_linha["VAL_COMISSAO"] = row_original["Valor Seguro"]
            nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Proposta"]
            nova_linha["PCL_COMISSAO"] = row_original["% Seguro"]
            novas_linhas.append(nova_linha)

        # Criar linha Pré-Adesão
        if pd.isna(row_original.get("Comissao por Emissão", 0)) == False:
            if row_original["Comissao por Emissão"] != 0:
                nova_linha = row_mapeada.copy()
                nova_linha["TIPO_COMISSAO_BANCO"] ="PRÉ ADESÃO"
                nova_linha["VAL_COMISSAO"] = row_original["Comissao por Emissão"]
                nova_linha["VAL_BASE_COMISSAO"] = row_original["Comissao por Emissão"]
                nova_linha["PCL_COMISSAO"] = 1
                novas_linhas.append(nova_linha)

        # Criar linha Comissão
        if pd.isna(row_original.get("$ Comissão")) == False:
            nova_linha = row_mapeada.copy()

            if row_original["$ Comissão"] < 0:
                nova_linha["TIPO_COMISSAO_BANCO"] ="ESTORNO"
            else:
                nova_linha["TIPO_COMISSAO_BANCO"] ="DIRETA"

            if (row_original["% Comissao"] == 0):
                nova_linha["VAL_BASE_COMISSAO"] = 0
            else:
                nova_linha["VAL_BASE_COMISSAO"] = row_original["Valor Proposta"]

            nova_linha["VAL_COMISSAO"] = row_original["$ Comissão"]
            nova_linha["PCL_COMISSAO"] = row_original["% Comissao"]
            novas_linhas.append(nova_linha)

        return novas_linhas

    def run(self, df):
        try:
            df = self.readArchive(df)

            infos ={
                "Nr Proposta": "NUM_PROPOSTA",
                "Data Status": "DAT_CREDITO",
                "Observações": "DSC_OBSERVACAO"
            }

            logger.info("Validando dataframe")

            Error = validDf(df, infos)
            if Error:
                return Error

            logger.info("Dataframe validado")
            logger.info("Criando Dataframe")

            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            logger.info("Dataframe criado com sucesso")
            logger.info("Adicionando valores de forma fixa")

            df_novo["NUM_BANCO"] = '7996'
            df_novo["NOM_BANCO"] = 'AMIGOZ'
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

            linhas_expandidas = []
            for index, row_original in df.iterrows():
                row_mapeada = df_novo.loc[index].to_dict() if index < len(df_novo) else {}
                linhas_expandidas.append(row_mapeada)
                linhas_expandidas.extend(self.expandir_linhas(row_original, row_mapeada))

            df_novo = pd.DataFrame(linhas_expandidas)

            if "DSC_OBSERVACAO" in df_novo.columns:
                mask = df_novo["DSC_OBSERVACAO"] == "Credito devido estorno feito em duplicidade"
                df_novo.loc[mask, "TIPO_COMISSAO_BANCO"] = "REEMBOLSO"

            df_novo = df_novo[df_novo["TIPO_COMISSAO_BANCO"].notna()]
            df_novo = df_novo[df_novo["VAL_COMISSAO"].notna()]
            return df_novo
        except:
            logger.exception("Erro ao editar Amigoz")
            logger.error("Erro ao editar Amigoz")
            return "Erro ao editar Amigoz"
        finally:
            logger.info("Finalizado processo de edicao Amigoz")