import pandas as pd
import cols_opcoes

def kardbank(df):

    df = pd.read_html(df, header=0)[0]

    infos ={
        "Número Ade":"NUM_PROPOSTA",
        "Data Pgto Vendedor":"DAT_CREDITO",
        "Valor Bruto":"VAL_BASE_COMISSAO",
        "% Comissão":"PCL_COMISSAO",       
    }

    if not isinstance(df, pd.DataFrame):
        return"Erro: A entrada não é um DataFrame válido."
    
    
    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return"Erro: Colunas necessárias não encontradas no DataFrame."
    
    df_novo = pd.DataFrame(columns=cols_opcoes.COL_OPCOES)

    for col_origem, col_destino in infos.items():
        if col_origem in df.columns:
            df_novo[col_destino] = df[col_origem]

    valores_tratados = []

    for valor in df_novo["VAL_BASE_COMISSAO"]:    
        
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)
            valor_teste = valor_str.replace("R$ ", "")
            valor_teste = valor_teste.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)
    
    df_novo["VAL_BASE_COMISSAO"] = valores_tratados

    df_novo["NOM_BANCO"] = "KARDBANK"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["VAL_BRUTO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["VAL_COMISSAO"] = df_novo["VAL_BASE_COMISSAO"] * (df_novo["PCL_COMISSAO"] / 100)
    df_novo["NUM_BANCO"] = 6910
    df_novo["VAL_LIQUIDO"] = df_novo["VAL_BASE_COMISSAO"]
    df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"

    return df_novo