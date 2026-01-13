import pandas as pd
from datetime import datetime
import cols_opcoes

def digio(df):
    
    df = pd.read_csv(df, sep=";")

    data = datetime.now().strftime("%d/%m/%Y")

    infos = {
        "Prop.": "NUM_PROPOSTA",
        "Base de Cálculo": "VAL_BASE_COMISSAO",
        "Valor Comiss": "VAL_COMISSAO",
        "Parâm": "PCL_COMISSAO",
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    df_novo = pd.DataFrame(columns=cols_opcoes.COL_OPCOES)

    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["VAL_BASE_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["VAL_COMISSAO"] = df_novo["VAL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["DAT_CREDITO"] = data
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["NUM_BANCO"] = 335
    df_novo["NOM_BANCO"] = "BANCO DIGIO"
    df_novo["PCL_COMISSAO"] = (df_novo["PCL_COMISSAO"].astype(str).str.replace(",", ".").astype(float) * 100)

    return df_novo
    