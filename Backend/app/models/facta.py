import pandas as pd
import requests

def facta(df):
    df = pd.read_excel(df, engine="openpyxl")

    session = requests.Session()
    bruto_por_proposta = {}
    list_props = []

    for idx in df.index:
        obs = str(df.at[idx, "OBSERVACAO"])
        proposta = df.at[idx, "CODIGOAF"]

        list_props.append(proposta)
        if "PGTO ADIANTAMENTO" in obs and proposta not in bruto_por_proposta:
            try:
                response = session.get(
                    f"http://192.168.1.252:3004/v1/wb-api/proposta/?proposal={proposta}",
                    timeout=10
                )
                data = response.json()

                if data[0]["tipo"] == "PORTAB/REFIN":
                    bruto_por_proposta[proposta] = data[0]["bruto"]

            except Exception as e:
                print(f"Erro proposta {proposta}: {e}")

    df["VLRAF"] = df["CODIGOAF"].map(bruto_por_proposta).fillna(df["VLRAF"])

    valores_tratados = []

    for valor in df["VLRAF"]:
        valor_str = valor

        if type(valor) == str :

            valor_str = str(valor)

            valor_teste = valor_str.replace(".", "")
            valor_teste = valor_teste.replace(",", ".")
            valor_str = float(valor_teste)

        valores_tratados.append(valor_str)

    df["VLRAF"] = valores_tratados

    return df