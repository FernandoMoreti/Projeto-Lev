import pandas as pd
import cols_opcoes

def grandino(df):

    df = pd.read_csv(df, sep=";")

    infos ={
       "Nro Proposta":"NUM_PROPOSTA",
       "Data de Fechamento":"DAT_CREDITO",
       "Base de Cálculo":"VAL_BASE_COMISSAO",
       "Valor Comissão":"VAL_COMISSAO",
       "Porcentagem":"PCL_COMISSAO"
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=cols_opcoes.COL_OPCOES)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    df_novo["NUM_BANCO"] = '88888'
    df_novo["NOM_BANCO"] = 'GRANDINO LTDA'
    df_novo["TIPO_COMISSAO_BANCO"] = 'DIRETA'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    return df_novo