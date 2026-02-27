from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from .models import bancos, banks
from dotenv import load_dotenv
import os
from .logger import setup_logging, setup_error_logging
import requests
from io import BytesIO
from datetime import datetime, date

load_dotenv()

bancos_logger = setup_logging("bancos", "bancos.log")
infos_logger = setup_logging("infos", "infos.log")
setup_error_logging()


app = Flask(__name__) #cria o app, inicializa a aplicação flask
CORS(app, origins=["https://projeto-lev.vercel.app", "http://localhost:5173"], expose_headers=["Content-Disposition"])

@app.route("/execute", methods=["POST"])
def execute():

    try:

        infos_logger.info("Iniciando o sistema de envio do arquivo para edicao")

        nome_banco = request.form.get("banco")
        arquivo = request.files.get("arquivo")
        nome_banco = nome_banco.split(" ")[0].lower()

        if not nome_banco:
            infos_logger.warning("Nao foi recebido nenhum Banco")
            return jsonify({"erro": "Não recebemos um valor para o nome do banco"}), 400

        if  not arquivo:
            infos_logger.warning("Nao foi recebido nenhum arquivo")
            return jsonify({"erro": "Não recebemos um valor de arquivo"}), 400

        if nome_banco not in bancos:
            infos_logger.error("Nao foi localizado o banco %s no nosso sistema", nome_banco)
            return jsonify({"erro": f"Função não encontrada para o banco: {nome_banco}"}), 400

        infos_logger.info("Arquivo: %s do banco %s enviado para tratamento", arquivo, nome_banco)
        resultado = bancos[nome_banco](arquivo)


        if type(resultado) is str:
            infos_logger.error(f"Recebemos um retorno inesperado da funcao: {resultado}")
            return jsonify({"erro": resultado}), 400

        infos_logger.info("Recebemos um retorno valido e OK da funcao")

        output = BytesIO()
        resultado.to_excel(output, index=False)
        output.seek(0)
        nome_banco = nome_banco.upper()

        infos_logger.info("Arquivo convertido em excel e enviado para download")

        # Criar nome do arquivo
        data_arquivo = datetime.now().strftime("%d-%m %H%M%S")
        nome_arquivo = f"{nome_banco} - {data_arquivo}.xlsx"

        # Enviar para download
        return send_file(
            output,
            mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            as_attachment=True,
            download_name=nome_arquivo
        )
    except Exception:
        infos_logger.exception("Erro crítico ao executar /execute")
        return jsonify({"error": "Erro interno inesperado"})
    finally:
        infos_logger.info("Finalizando o sistema de envio de arquivo para edicao e download")

@app.route("/groupProposal", methods=["POST"])
def groupProposal():

    try:
        nameBank = request.form.get("banco")
        nameBank = nameBank.lower().split("|")[0].replace(" ", "")
        queueId = request.form.get("queueId")

        



        # dfEdited = banks[nameBank].run(queueId)

        # archiveName = f"{nameBank}.xlsx"

        # tempDir = os.path.join(os.getcwd(), "temp")

        # os.makedirs(tempDir, exist_ok=True)

        # path = os.path.join(tempDir, archiveName)

        # dfEdited.to_excel(path, index=False)

        # return jsonify({
        #     "message": "Arquivo gerado e salvo com sucesso",
        #     "fileName": archiveName,
        #     "filePath": path
        # }), 200

    except Exception as e:
        print("Error")
        return jsonify({
            "error": "Erro interno ao processar e gerar o arquivo Excel.",
            "details": str(e)
        }), 500

# @app.route("/groupProposal", methods=["POST"])
# def groupProposal():

#     try:
#         nameBank = request.form.get("name")
#         nameBank = nameBank.lower()
#         queueId = request.form.get("queueId")

#         dfEdited = banks[nameBank].run(queueId)

#         archiveName = f"{nameBank}.xlsx"

#         tempDir = os.path.join(os.getcwd(), "temp")

#         os.makedirs(tempDir, exist_ok=True)

#         path = os.path.join(tempDir, archiveName)

#         dfEdited.to_excel(path, index=False)

#         return jsonify({
#             "message": "Arquivo gerado e salvo com sucesso",
#             "fileName": archiveName,
#             "filePath": path
#         }), 200

#     except Exception as e:
#         print("Error")
#         return jsonify({
#             "error": "Erro interno ao processar e gerar o arquivo Excel.",
#             "details": str(e)
#         }), 500



if __name__ == "__main__":
    app.run(debug=True)
