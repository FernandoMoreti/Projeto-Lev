import pandas as pd

def c6bankcreditomanual(df):
    df = pd.read_excel(df)

    validNames = ["DEVOLUÇÃO", "DEVOLUCAO"]

    for i, row in df.iterrows():
        motivo = str(row["Motivo"]).upper()
        if any(name in motivo for name in validNames) and row["Categoria"] == "REFIN PORT-PGTO COMISSAO FLAT":
            df.at[i, "Categoria"] = (f"{row['Categoria']}  reembolso")

        if row["Loja Recebedora"] != "LEV":
            df.at[i, "Valor Estorno"] = 0
            df.at[i, "Valor Total"] = 0
            df.at[i, "Valor Base"] = 0
            df.at[i, "Valor Líquido Crédito"] = 0

    df = df.drop(columns=["Valor Bruto Refin Portabilidade"])

    df["Valor Crédito"] = df["Valor Crédito"].astype(float)
    df["Valor Estorno"] = df["Valor Estorno"].astype(float)
    df["Valor Total"] = df["Valor Total"].astype(float)
    df["Valor Base"] = df["Valor Base"].astype(float)
    df["Valor Financiado"] = df["Valor Financiado"].astype(float)
    df["Valor Líquido Crédito"] = df["Valor Líquido Crédito"].astype(float)

    return df