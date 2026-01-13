import pandas as pd
import os

def meses(mes):

    meses= {
        "01": "JANEIRO",
        "02": "FEVEREIRO",
        "03": "MARÇO",
        "04": "ABRIL",
        "05": "MAIO",
        "06": "JUNHO",
        "07": "JULHO",
        "08": "AGOSTO",
        "09": "SETEMBRO",
        "10": "OUTUBRO",
        "11": "NOVEMBRO",
        "12": "DEZEMBRO"
    }

    return meses.get(mes, "Mês inválido")

def btw(df, cols_opcoes):
    numMes = (df.filename.split('_')[2].split('-')[0][4:6])
    mes = meses((df.filename.split('_')[2].split('-')[0][4:6]))
    ano = (df.filename.split('_')[2].split('-')[0][0:4])

    if df.filename.split('_')[1] == "BTW":
        name = "LECCA"
    else:
        name = "BTW"

    data = f"{name}_{df.filename.split('_')[2]}"

    caminho_pasta = f"Z:\COMISSÃO\DOCS - WORK BANK {ano}\BTW\\{numMes} - {mes}"
    arquivos = os.listdir(caminho_pasta)

    arquivo_encontrado = None

    for arquivo in arquivos:
        if data in arquivo:
            arquivo_encontrado = arquivo
            break
    
    if arquivo_encontrado:
        caminho_completo = os.path.join(caminho_pasta, arquivo_encontrado)
        df_encontrado = pd.read_excel(caminho_completo)
    else:
        return "Arquivo não encontrado para a data:", data

    df = pd.read_excel(df)


    if name == "LECCA":
        df_encontrado.rename(columns={
            "Vr_Comissao_Flat_Bruto" : "Total_Bruto",
            "Tx_Comissao_Flat" : "Tx_Serviço"
        }, inplace=True)
        df_encontrado['tipo'] = 'DIRETA'
        df['tipo'] = 'BÔNUS'
    else: 
        df_encontrado.rename(columns={
            "Total_Bruto" : "Vr_Comissao_Flat_Bruto",
            "Tx_Serviço" : "Tx_Comissao_Flat",
        }, inplace=True)
        df_encontrado['tipo'] = 'BÔNUS'
        df['tipo'] = 'DIRETA'


    df = pd.concat([df_encontrado, df], ignore_index=True)

    if name == "LECCA":
        infos = {
            "Proposta": "NUM_PROPOSTA",
            "DT_Pagamento": "DAT_CREDITO",
            "Valor_Liberado": "VAL_BASE_COMISSAO",
            "Total_Bruto": "VAL_COMISSAO",
            "Tx_Serviço": "PCL_COMISSAO",
            "tipo": "TIPO_COMISSAO_BANCO",
        }
    else: 
        infos = {
            "Proposta": "NUM_PROPOSTA",
            "DT_Pagamento": "DAT_CREDITO",
            "Valor_Liberado": "VAL_BASE_COMISSAO",
            "Vr_Comissao_Flat_Bruto": "VAL_COMISSAO",
            "Tx_Comissao_Flat": "PCL_COMISSAO",
            "tipo": "TIPO_COMISSAO_BANCO",
        }

    if not isinstance(df, pd.DataFrame):
        return "Erro: A entrada não é um DataFrame válido."
    
    colunas_origem_presentes = all(col_origem in df.columns for col_origem in infos.keys())
    if not colunas_origem_presentes:
        return "ErroColunas"
    
    df_novo = pd.DataFrame(columns=cols_opcoes)

    for col_origem, col_destino in infos.items():
        df_novo[col_destino] = df[col_origem]
    
    df_novo["NUM_BANCO"] = 10501
    df_novo["NOM_BANCO"] = "BTW BANK"
    df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
    df_novo["PCL_COMISSAO"] = df_novo["PCL_COMISSAO"] * 100

    return df_novo