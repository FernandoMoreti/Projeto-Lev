import pandas as pd
from ..utils import createDataframe, inputValueColumns, validDf

def c6bank(df):
    df = pd.read_excel(df)

    validNames = ["DEVOLUÇÃO", "DEVOLUCAO", "ESTORNO"]

    for i, row in df.interrows():
        if row["Situação"] in validNames or row["Categoria"] in validNames or row["adasd"] in validNames:
            pass
