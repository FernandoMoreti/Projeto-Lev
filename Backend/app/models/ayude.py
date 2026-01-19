# import pandas as pd
# from ..utils import createDataframe, inputValueColumns, validDf
# from .bank import Bank

# # class Ayude:
# #     def __init__(self, name, num, type):
# #         super().__init__(name, num, type)

# # def ayude(df):

# #     df_soli = pd.read_excel(df, sheet_name="DADOS DA SOLICITAÇÃO", )
# #     df = pd.read_excel(df, sheet_name="PROPOSTAS PRÓPRIAS", )
# #     df = df.iloc[:-3]

# #     infos ={
# #        "ID DA PROPOSTA":"NUM_PROPOSTA",
# #        "VALOR DA PROPOSTA":"VAL_BASE_COMISSAO",
# #        "VALOR DA COMISSÃO":"VAL_COMISSAO"
# #     }

# #     Error = validDf(df, infos)
# #     if Error:
# #         return Error

# #     df_novo = createDataframe()

# #     df_novo = inputValueColumns(df, df_novo, infos)

# #     df_novo["NUM_BANCO"] = '1723'
# #     df_novo["NOM_BANCO"] = 'AYUDE'
# #     df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
# #     df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
# #     df_novo["DAT_CREDITO"] = df_soli["SOLICITADO EM"]
# #     df_novo["PCL_COMISSAO"] = df_novo["VAL_COMISSAO"] / df_novo["VAL_BASE_COMISSAO"] * 100

# #     return df_novo


## PAUSADO POR TEMPO INDETERMINADO