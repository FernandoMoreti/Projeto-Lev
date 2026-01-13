import pandas as pd
import cols_opcoes

def euro(df):
    
    df = pd.read_excel(df)

    infos = {
        "PROPOSTA":"NUM_PROPOSTA",
        "VALOR LIBERADO R$":"VAL_BASE_COMISSAO",
        "% PAR":"PCL_COMISSAO",
        "COMISSÃO PARCEIRO":"VAL_COMISSAO",
        "DATA DE PAGAMENTO":"DAT_CREDITO",
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

    tamanho = len(df_novo["NUM_PROPOSTA"])

    df_novo = df_novo.drop(index=[tamanho -1, tamanho -2])

    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
    df_novo["NUM_BANCO"] = "359108"
    df_novo["NOM_BANCO"] = "EURO17 EMPRESARIAL"

    return df_novo
    