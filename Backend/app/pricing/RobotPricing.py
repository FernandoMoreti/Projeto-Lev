from abc import ABC
from datetime import datetime

import pandas as pd

class RobotPricing(ABC):

    def __init__(self):
        pass

    def createHash(archiveWork, archiveBank, columnIdTable, columnPrazo, percComission):
        listOfHashWork = []
        listOfHashBank = []

        for index, row in archiveWork.iterrows():
            compareValue = f"{row['Id Tabela Banco']}-{row['Parc. Atual'].split('-')[0]}"
            listOfHashWork.append({
                'index': index,
                'compareValue': compareValue,
                '% comissao': row["% Comissão"]
            })

        for index, row in archiveBank.iterrows():
            compareValue = f"{row[columnIdTable]}-{row[columnPrazo]}"
            listOfHashBank.append({
                'index': index,
                'compareValue': compareValue,
                '% comissao': row[percComission],
                'dateClose': row["Fim"] or None
            })

        return listOfHashWork, listOfHashBank

    def getAllTablesToChange(self, fileWork, fileBank):
        try:

            dfWork = pd.read_excel(fileWork)
            dfBank = pd.read_excel(fileBank, header=2)

            dfWork['chave_busca'] = dfWork["Id Tabela Banco"] + '-' + dfWork["Parc. Atual"].split("-")[0]

            editLines = []
            newLines = []
            closeLines = []

            for index, row in dfBank.iterrows():
                key = row["CÓDIGO CONVÊNIO/TABELA"] + '-' + row["PRAZO"]

                if key in dfWork['chave_busca'].values:
                    editLines.append(row)
                    closeLines.append(row)


        except Exception as e:
            print("Error ao ler os arquivos")
            print(str(e))

    def run(self, fileWork, fileBank):
        try:
            print("Iniciando o processo de validação das tabelas")
            self.getAllTablesToChange(fileWork, fileBank)
            print("Processo de validação das tabelas finalizado com sucesso")
        except Exception as e:
            print("Error ao validar as tabelas")
            print(str(e))
