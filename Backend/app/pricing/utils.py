import pandas as pd
from datetime import datetime

def getTables(listOfHashWork, listOfHashBank, openTables, closeTables):

    values = set(item['compareValue'] for item in listOfHashWork)

    openTables = [
        {'index': item['index'], 'compareValue': item['compareValue']}
        for item in listOfHashBank if item['compareValue'] not in values
    ]

    closeTables = addCloseTables(listOfHashWork, listOfHashBank, openTables, closeTables)


    return closeTables, openTables

def addOpenTables(openTables, value):
    openTables.append(value)

def addCloseTables(listOfHashWork, listOfHashBank, openTables, closeTables):
    # Mapas de comissão e índice da Work
    work_map = {
        item['compareValue']: normalizeCommission(item['% comissao'])
        for item in listOfHashWork
    }

    work_index_map = {
        item['compareValue']: item['index']
        for item in listOfHashWork
    }

    # Mapa de comissão do Bank
    bank_map = {
        item['compareValue']: normalizeCommission(item['% comissao'])
        for item in listOfHashBank
    }

    bank_values = set(bank_map.keys())
    common_values = set(work_map.keys()) & set(bank_map.keys())

    # 1️⃣ Adiciona no closeTables itens que existem na Work mas não no Bank
    for item in listOfHashWork:
        cv = item['compareValue']
        if cv not in bank_values:
            closeTables.append({
                'indexOfTableWork': work_index_map[cv],  # ajuste para Excel
                'compareValue': cv,
                '% comissao_work': work_map[cv],
                '% comissao_bank': None,
                'dateClose': "Não existe no bank"
            })

    # 2️⃣ Adiciona no closeTables itens que existem em ambos, mas com diferença
    for item in listOfHashBank:
        cv = item['compareValue']
        if cv not in common_values:
            continue

        comissao_diferente = bank_map[cv] != work_map[cv]
        tabela_fechada = pd.notna(item.get('dateClose'))

        if comissao_diferente or tabela_fechada:
            if comissao_diferente:
                # adiciona no openTables caso a comissão seja diferente
                addOpenTables(openTables, {
                    'index': item["index"],
                    'compareValue': cv,
                })

            date_close = item.get('dateClose') if pd.notna(item.get('dateClose')) else datetime.now()

            closeTables.append({
                'indexOfTableWork': work_index_map[cv],
                'compareValue': cv,
                '% comissao_work': work_map[cv],
                '% comissao_bank': bank_map[cv],
                'dateClose': date_close
            })

    return closeTables

def normalizeCommission(value):
    if value is None:
        return None
    return float(
        str(value)
        .replace('%', '')
        .replace(',', '.')
        .strip()
    )