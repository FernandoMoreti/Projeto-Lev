# import pandas as pd
# from ..utils import convertValues
# import logging
# from .bank import Bank
# from ..mapper import FACTA

# logger = logging.getLogger("bancos")

# class Facta(Bank):
#     def __init__(self, name = "FACTA", num = 0, type = "excel"):  # num não especificado, coloquei 0
#         super().__init__(name, num, type)

#     def readArchive(self, df):
#         try:
#             df = pd.read_excel(df, engine="openpyxl")
#             df = df[df["TIPOCONTACORRETOR"] != 12]
#             df = df[df["TIPOCONTACORRETOR"] != 30]
#             df = df[df["TIPOCONTACORRETOR"] != 78]
#             df = df[df["TIPOCONTACORRETOR"] != 81]

#             print(df)
#             return df
#         except Exception:
#             logger.exception("Erro ao ler arquivo")
#             logger.error("Erro ao ler arquivo")
#             return "Erro ao ler arquivo"
#         finally:
#             logger.info("Finalizando processo de leitura do arquivo")

#     def run(self, df):

#         try:
#             df = self.readArchive(df)

#             infos ={
#                 "CODIGOAF":"NUM_PROPOSTA",
#                 "VLRAF":"VAL_BASE_COMISSAO",
#                 "DEBITO":"VAL_LIQUIDO",
#                 "CREDITO":"VAL_COMISSAO",
#                 "DATA":"DAT_CREDITO",
#                 "TABELA" :"COD_UNIDADE_EMPRESA",
#                 "DS_TIPOLANCAMENTO" :"COD_BANCO",
#                 "TIPOCONTACORRETOR": "TIPO_COMISSAO_BANCO",
#             }

#             logger.info("Validando DataFrame")
#             Error = self.validDataframe(df, infos)
#             if Error:
#                 return Error

#             logger.info("Criando novo DataFrame")
#             df_novo = self.createDataframe()
#             df_novo = self.inputValues(df, df_novo, infos)

#             df_novo["VAL_BASE_COMISSAO"] = convertValues(df_novo, "VAL_BASE_COMISSAO")
#             df_novo["VAL_LIQUIDO"] = convertValues(df_novo, "VAL_LIQUIDO")
#             df_novo["VAL_COMISSAO"] = convertValues(df_novo, "VAL_COMISSAO")

#             listValidValues = []
#             listType = []
#             listOfDescription = []

#             for index, row in df_novo.iterrows():
#                 if row["VAL_LIQUIDO"] != 0 and pd.notna(row["VAL_LIQUIDO"]):
#                     listValidValues.append(row["VAL_LIQUIDO"])
#                 else:
#                     listValidValues.append(row["VAL_COMISSAO"])

#                 description = row["COD_BANCO"] + " - " + row["COD_UNIDADE_EMPRESA"]
#                 listOfDescription.append(description)

#                 type = FACTA[row["TIPO_COMISSAO_BANCO"]]
#                 listType.append(type)

#             df_novo["TIPO_COMISSAO_BANCO"] = listType
#             df_novo["VAL_COMISSAO"] = listValidValues
#             df_novo["DSC_OBSERVACAO"] = listOfDescription

#             df_novo["NOM_BANCO"] = "FACTA FINANCEIRA"
#             df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
#             df_novo["NUM_BANCO"] = 0
#             df_novo["VAL_LIQUIDO"] = None
#             df_novo["COD_BANCO"] = None
#             df_novo["COD_UNIDADE_EMPRESA"] = None
#             df_novo["PCL_COMISSAO"] = (df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"]) * 100

#             return df_novo
#         except Exception:
#             logger.exception("Erro ao editar Facta")
#             logger.error("Erro ao editar Facta")
#             return "Erro ao editar Facta"
#         finally:
#             logger.info("Finalizado processo de edicao Facta")