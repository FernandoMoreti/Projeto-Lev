from ..mapper import Mapper
import json

class C6bankMapper(Mapper):

    def map(self, line):
        model = self.createNullModel()

        model["NUM_PROPOSTA"] = line.get('Número Proposta')
        model["NUM_CONTRATO"] = line.get('Número Proposta')
        model["DAT_CREDITO"] = line.get('Data Pagamento')
        model["VAL_BASE_COMISSAO"] = line.get('Valor Base')
        model["VAL_BRUTO"] = line.get('Valor Financiado')
        model["VAL_COMISSAO"] = line.get('Valor Bruto')
        model["DSC_OBSERVACAO"] = line.get('Motivo')
        model["QTD_PARCELA"] = line.get('Parcelas')
        model["DSC_TIPO_COMISSAO"] = line.get('Débito/Crédito')
        model["DSC_SITUACAO_BANCO"] = line.get('Categoria')
        model["COD_BANCO"] = line.get('Nome Comissionado')
        model["DSC_PRODUTO"] = line.get('Tarifas Adicionais')
        model["PCL_COMISSAO"] = line.get('Perc à Vista')

        model["NOM_BANCO"] = "C6 BANK"
        model["NUM_BANCO"] = "336"

        return json.dumps(model, ensure_ascii=False, default=str)
