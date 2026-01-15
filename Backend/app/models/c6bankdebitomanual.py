import pandas as pd

def c6bankdebitomanual(df):
    df = pd.read_excel(df)

    listMotivo = {
        "Estorno - Pag Duplicado - Comissao Port": "EST DUPLICIDADE EST PGTO COMISSAO FLAT",
        "Estorno - Pagamento de Complemento de TC e Seguro - Manual Indevido": "ESTORNO TAXA",
        "Estorno - Devolucao de pendencia FÝsico - ComissÒo ficou a maior": "AJUSTE DE PAGAMENTO A MAIOR",
        "Ajuste de Pagamento A Maior": "Ajuste de Pagamento A Maior",
    }

    for i, row in df.iterrows():
        if row["Loja Recebedora"] != "LEV":
            df.at[i, "Valor Total"] = 0

    for i, motivo in listMotivo.items():
        if row["Motivo"] == motivo:
            df.at[i, "Categoria"] = listMotivo[row["Motivo"]]
            df.at[i, "Situação"] = listMotivo[row["Motivo"]]

    df["Valor Débito"] = df["Valor Débito"].astype(float)
    df["Valor Estorno"] = df["Valor Estorno"].astype(float)
    df["Valor Total"] = df["Valor Total"].astype(float)

    return df