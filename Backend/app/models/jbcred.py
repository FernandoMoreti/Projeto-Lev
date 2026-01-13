import pandas as pd
from datetime import datetime

def jbcred(df, cols_opcoes):

    now = datetime.now()
    current_date = now.strftime("%d/%m/%Y")

    df = pd.read_html(df, header=0)[0]

    infos ={
        "NRCONTRATO":"NUM_PROPOSTA",
        "VLR_OPER":"VAL_BASE_COMISSAO",
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    df_novo = pd.DataFrame(columns=cols_opcoes)

    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    num_propostas = []

    for num in df_novo["NUM_PROPOSTA"]:
        num_str = str(num)
        num_str = num_str.replace("-", "")
        num_str = float(num_str)
        num_propostas.append(num_str)
        
    df_novo["NUM_PROPOSTA"] = num_propostas
    df_novo["DAT_CREDITO"] = current_date
    df_novo["NOM_BANCO"] = "JBCRED"
    df_novo["PCL_COMISSAO"] = 10
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] / 10
    df_novo["NUM_BANCO"] = 777
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo