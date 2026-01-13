import pandas as pd


def happy(df, cols_opcoes):

    df = pd.read_excel(df, header=2)

    infos ={
       "PROPOSTA":"NUM_PROPOSTA",
       "DT PAGTO":"DAT_CREDITO",
       "VR BASE":"VAL_BASE_COMISSAO",
       "VR CMS":"VAL_COMISSAO",
       "% CMS":"PCL_COMISSAO",       
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."

    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"ErroColunas"

    # Criar o DataFrame com as colunas desejadas
    df_novo = pd.DataFrame(columns=cols_opcoes)

    # Mapeamento de colunas
    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

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

    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["NUM_BANCO"] = 1010
    df_novo["NOM_BANCO"] = 'HAPPY'
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]

    for i in range(len(df_novo["VAL_BASE_COMISSAO"])):
        if df_novo["VAL_BASE_COMISSAO"][i] < 0:
            df_novo.loc[i, "TIPO_COMISSAO_BANCO"] = 'ESTORNO'
        else:
            df_novo.loc[i, "TIPO_COMISSAO_BANCO"] = 'DIRETA'
            
    return df_novo