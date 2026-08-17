import pandas as pd
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

col_opcoes = [
   "NUM_BANCO",
   "NOM_BANCO",
   "NUM_PROPOSTA",
   "NUM_CONTRATO",
   "NOM_CLIENTE",
   "COD_CPF_CLIENTE",
   "DSC_PRODUTO",
   "DSC_SITUACAO_BANCO",
   "DSC_OBSERVACAO",
   "DAT_CREDITO",
   "VAL_BRUTO",
   "VAL_LIQUIDO",
   "VAL_SALDO_REFINANCIAMENTO",
   "VAL_BASE_COMISSAO",
   "VAL_COMISSAO",
   "PCL_COMISSAO",
   "DSC_TIPO_COMISSAO",
   "COD_LOJA",
   "COD_UNIDADE_EMPRESA",
   "COD_BANCO",
   "COD_TIPO_PROPOSTA_EMPRESTIMO",
   "DSC_TIPO_PROPOSTA_EMPRESTIMO",
   "NIC_CTR_USUARIO",
   "COD_PRODUTO",
   "COD_PRODUTOR_VENDA",
   "COD_PRODUTOR_VENDA_BANCO",
   "COD_TIPO_COMISSAO",
   "COD_SITUACAO_EMPRESTIMO",
   "QTD_PARCELA",
   "NUM_PARCELA_DIFERIDA_EMPRESA",
   "DAT_EMPRESTIMO",
   "DAT_CONFIRMACAO",
   "DAT_ESTORNO",
   "DAT_CTR_INCLUSAO",
   "TIPO_COMISSAO_BANCO",
   "PCL_TAXA_EMPRESTIMO"
]

def createDataframe():
    newDataFrame = pd.DataFrame(columns=col_opcoes)
    return newDataFrame

def validDf(df, infos):

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())

    if not colunas_origem_presentes:
        return"ErroColunas"

def inputValueColumns(df, df_novo, infos):
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    return df_novo

def convertValues(df_novo, columns):
    valores_tratados = []

    for valor in df_novo[columns]:
        valor_str = valor

        try:
            v = str(valor).replace("R$", "").strip()
            if "," in v and "." in v:
                v = v.replace(".", "").replace(",", ".")
            elif "," in v:
                v = v.replace(",", ".")

            if "-" in v:
                v = v.replace("-", "").strip()
                v = "-" + v

            valor_str = float(v)

            valores_tratados.append(valor_str)
        except (ValueError, TypeError):
            valores_tratados.append(0.0)

    return valores_tratados

def paintLine(row):
    if row["NUM_PROPOSTA"] == 0:
        return ["background-color: #ffcccc"] * len(row)
    return [""] * len(row)

def createListByLine(df):
    listOfProposal = []

    for index, row in df.iterrows():

        if pd.isna(row["NUM_PROPOSTA"]) or pd.isna(row["VAL_COMISSAO"]):
            return "Propostas sem valor de numero de proposta ou valor de comissao"

        if pd.isna(row["DAT_CREDITO"]):
            row["DAT_CREDITO"] = datetime.now().strftime("%d/%m/%Y")

        row["DAT_CREDITO"] = datetime.strptime(row["DAT_CREDITO"], "%d/%m/%Y").date()

        data = {
            "bank": row["NOM_BANCO"],
            "proposal": row["NUM_PROPOSTA"],
            "date": row["DAT_CREDITO"],
            "valBase": round(row["VAL_BASE_COMISSAO"], 2),
            "valCommission": round(row["VAL_COMISSAO"], 2),
            "pclCommission": round(row["PCL_COMISSAO"], 2),
            "typeCommission": row["TIPO_COMISSAO_BANCO"],
        }

        listOfProposal.append(data)

    return listOfProposal