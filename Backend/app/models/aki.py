import pandas as pd
import Backend.app.models.cols_opcoes as cols_opcoes


def aki(df):

    data = df.filename.split("_")[0]
    resultado = f"{data[:2]}/{data[3:5]}/{data[6:]}"

    df = pd.read_excel(df)

    infos = {
        "Nº Contrato": "NUM_PROPOSTA",
        "Valor Total": "VAL_BASE_COMISSAO",
        "% Comissão": "PCL_COMISSAO",
        "Valor Comissão": "VAL_COMISSAO",
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

    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100
    df_novo["DAT_CREDITO"] = resultado
    df_novo["NUM_BANCO"] = 1684
    df_novo["NOM_BANCO"] = "AKI CAPITAL"
    
    return df_novo
