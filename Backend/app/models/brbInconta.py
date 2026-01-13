import pandas as pd
import camelot
import Backend.app.models.cols_opcoes as cols_opcoes

def brbInconta(df):

    tables = camelot.read_pdf(df, pages='all',flavor="stream")

    if not tables:
        return "Nenhuma tabela encontrada no PDF"
    
    for index, t in enumerate(tables):
        if index == 1:
            t.df = t.df.drop(columns=[1])
            t.df = t.df.drop(columns=[2])
            print(t.df)
            t.df = t.df.dropna(axis=1, how="all")
            print(t.df)
            t.df.rename(columns={i: i-1 for i in range(1, t.df.shape[0])}, inplace=True)
        if len(t.df[0]) > 45:
            t.df = t.df.drop(columns=[1])
        else:
            t.df = t.df.iloc[6:]
            print(t.df)

    df = pd.concat([t.df for t in tables], ignore_index=True)

    df = df.replace(r'^\s*$', pd.NA, regex=True)

    df = df.dropna(thresh=8) # remove linhas que tenham pelo menos 10 colunas preenchidas

    infos = {
        2 : "NUM_PROPOSTA",
        7 : "VAL_BASE_COMISSAO",
        8 : "VAL_COMISSAO",
        5 : "PCL_COMISSAO",
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

    df_novo = df_novo.iloc[:-1]

    valores_tratados = []

    for valor in df_novo["VAL_BASE_COMISSAO"]:    
        
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)
    
    df_novo["VAL_BASE_COMISSAO"] = valores_tratados
    
    valores_tratados = []

    for valor in df_novo["VAL_COMISSAO"]:    
        
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)
    
    df_novo["VAL_COMISSAO"] = valores_tratados

    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"].astype(str).str.replace(",", ".").astype(float)

    df_novo["NUM_PROPOSTA"] = df_novo["NUM_PROPOSTA"].astype(int)
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["NUM_BANCO"] = 70
    df_novo["NOM_BANCO"] = 'BRB - BANCO DE BRASÍLIA'
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo