import pandas as pd
import logging
from .bank import Bank
from datetime import datetime

logger = logging.getLogger("bancos")

class ComissaoZerada(Bank):
    def __init__(self, name = "CAIXA", num = 104, type = "excel"):
        super().__init__(name, num, type)

    def readArchive(self, df):
        try:
            df = pd.read_excel(df)
            return df
        except Exception:
            logger.exception("Erro ao ler arquivo")
            logger.error("Erro ao ler arquivo")
            return "Erro ao ler arquivo"
        finally:
            logger.info("Finalizando processo de leitura do arquivo")

    def run(self, df):

        try:

            df = self.readArchive(df)

            infos ={
                "BANCO": "NOM_BANCO",
                "PROPOSTA":"NUM_PROPOSTA",
                "VR BASE REPASSE":"VAL_BASE_COMISSAO",
            }

            mapperName = {
                "AGIBANK": "BANCO AGIBANK S.A.",
                "AKI CAPITAL": "AKI CAPITAL",
                "AMIGOZ": "AMIGOZ",
                "BANRISUL": "BANCO BANRISUL S/A",
                "BMG": "BANCO BMG S.A.",
                "BRB - 360": "BRB - BANCO DE BRASÍLIA - 360",
                "BRB - INCONTA": "BRB - BANCO DE BRASÍLIA - INCONTA",
                "BTW BANK": "BTW BANK",
                "BV": "BV FINANCEIRA",
                "C6 BANK": "C6 BANK",
                "C6 AUTO": "C6 BANK AUTO",
                "CAIXA": "CAIXA ECONÔMICA FEDERAL",
                "CREDITAS": "CREDITAS",
                "CREFAZ": "CREFAZ",
                "CREFISA": "BANCO CREFISA S.A.",
                "DAYCOVAL": "BANCO DAYCOVAL S.A.",
                "DIGA CONSIG": "DIGA CONSIG",
                "DIGIO": "BANCO DIGIO",
                "EMPRESTEI CARD": "EMPRESTEI CARD",
                "EURO": "EURO17 EMPRESARIAL",
                "EVOL": "EVOL",
                "FACTA FINANCEIRA": "FACTA S.A.",
                "FIT ENERGIA": "FIT ECONOMIA DE ENERGIA S.A.",
                "GRANDINO BANK": "GRANDINO LTDA",
                "HAPPY": "HAPPY CONSIGNADO",
                "HOPE": "HOPE",
                "ICRED": "ICRED",
                "ITAU": "BANCO ITAU CONSIGNADO SA",
                "JBCRED": "JBCRED S/A",
                "KARDBANK": "KARDBANK CONSIGNADO FIDC",
                "MERCANTIL": "BANCO MERCANTIL DO BRASIL",
                "MEUCASHCARD": "MEUCASHCARD SERVIÇOS TECNOLÓGICOS E FINA",
                "NBC BANK": "NBC BANK",
                "NEO CREDITO": "NEO CREDITO",
                "NOVO SAQUE": "NOVO SAQUE",
                "NYC BANK": "NYC BANK",
                "OLE": "BANCO OLE",
                "PAN": "BANCO PAN",
                "PARANA BANCO": "PARANÁ BANCO S.A.",
                "PH TECH": "PH TECH",
                "PRESENCA BANK": "PRESENCA BANK SCP",
                "QUALI BANK": "QUALI BANK",
                "QUERO MAIS CREDITO": "QUERO MAIS CREDITO",
                "SABEMI": "SABEMI",
                "SAFRA": "BANCO J. SAFRA S.A.",
                "SANTANDER": "BANCO SANTANDER S.A.",
                "TOTALCASH": "TOTALCASH",
                "V8 DIGITAL": "V8 DIGITAL",
                "VCTEX": "VCTEX CORRESPONDENTE BANCARIO E MEIOS DE",
                "VEMCARD": "VEMCARD",
                "VIACERTA": "VIACERTA BANKING",
                "WEBCASH": "WEBCASH"
            }

            mapper  = {
                "BANCO AGIBANK S.A.": 121,
                "AKI CAPITAL": 1684,
                "AMIGOZ": 7996,
                "BANCO BANRISUL S/A": 41,
                "BANCO BMG S.A.": 318,
                "BRB - BANCO DE BRASÍLIA - 360": 701,
                "BRB - BANCO DE BRASÍLIA - INCONTA": 70,
                "BANCO OLE": 218,
                "BTW BANK": 10501,
                "BV FINANCEIRA": 44,
                "C6 BANK": 336,
                "C6 BANK AUTO": 3336,
                "CAIXA ECONÔMICA FEDERAL": 104,
                "CREDITAS": 88,
                "CREFAZ": 1964,
                "BANCO CREFISA S.A.": 69,
                "BANCO DAYCOVAL S.A.": 707,
                "DIGA CONSIG": 8888888,
                "BANCO DIGIO": 335,
                "EMPRESTEI CARD": 4444444,
                "EURO17 EMPRESARIAL": 359108,
                "EVOL": 7777,
                "FACTA S.A.": 149,
                "FIT ECONOMIA DE ENERGIA S.A.": 9173,
                "GRANDINO LTDA": 88888,
                "HAPPY CONSIGNADO": 1010,
                "HOPE": 1597,
                "ICRED": 329,
                "BANCO ITAU CONSIGNADO SA": 29,
                "JBCRED S/A": 777,
                "KARDBANK CONSIGNADO FIDC": 6910,
                "BANCO MERCANTIL DO BRASIL": 389,
                "MEUCASHCARD SERVIÇOS TECNOLÓGICOS E FINA": 666,
                "NBC BANK": 753,
                "NEO CREDITO": 3333333,
                "NOVO SAQUE": 1234,
                "NYC BANK": 1728,
                "BANCO PAN": 623,
                "PARANÁ BANCO S.A.": 254,
                "PH TECH": 8768,
                "PRESENCA BANK SCP": 482,
                "QUALI BANK": 2222222,
                "QUERO MAIS CREDITO": 3030,
                "SABEMI": 5,
                "BANCO J. SAFRA S.A.": 42,
                "BANCO SANTANDER S.A.": 351,
                "TOTALCASH": 1731,
                "V8 DIGITAL": 1725,
                "VCTEX CORRESPONDENTE BANCARIO E MEIOS DE": 1530,
                "VEMCARD": 1727,
                "VIACERTA BANKING": 7675,
                "WEBCASH": 1730
            }

            logger.info("Validando DataFrame")
            Error = self.validDataframe(df, infos)
            if Error:
                return Error

            logger.info("Criando novo DataFrame")
            df_novo = self.createDataframe()
            df_novo = self.inputValues(df, df_novo, infos)

            date = datetime.now().strftime("%d/%m/%Y")

            df_novo['NOM_BANCO'] = df_novo['NOM_BANCO'].map(mapperName)
            df_novo["NUM_BANCO"] = df_novo['NOM_BANCO'].map(mapper)
            df_novo["NUM_CONTRATO"] = df_novo["NUM_PROPOSTA"]
            df_novo["TIPO_COMISSAO_BANCO"] = "DIRETA"
            df_novo["PCL_COMISSAO"] = 0
            df_novo["VAL_COMISSAO"] = 0
            df_novo["DAT_CREDITO"] = date
            df_novo = df_novo.sort_values(by='NOM_BANCO')

            logger.info("Processamento do Caixa finalizado com sucesso")
            return df_novo
        except Exception:
            logger.exception("Erro ao editar Caixa")
            logger.error("Erro ao editar Caixa")
            return "Erro ao editar Caixa"
        finally:
            logger.info("Finalizado processo de edicao Caixa")