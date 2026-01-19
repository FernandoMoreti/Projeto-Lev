from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from .models import bancos
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
        nome_banco = nome_banco.lower()

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

@app.route("/getfile", methods=["GET"])
def getfile():

    today = date.today()

    user = {
        "email": os.environ.get("AUTH_LOGIN_EMAIL"),
        "password": os.environ.get("AUTH_LOGIN_PASSWORD")
    }

    getToken = requests.post(
        os.environ.get("URL_GET_TOKEN_LOGIN"),
        json=user
    )

    token = f'Bearer {getToken.json()["token"]}'
    banks = ["c6bankdebitomanual"]

    header = {
        "Authorization": token,
        "Content-Type": "application/json",
        "User-Agent": "insomnia/12.2.0"
    }

    for bank in banks:

        payload = {
            "s3Uri": f"s3://hives-116976060176/comission/{bank}/{today.year}/{today.month:02d}/{today.day:02d}/410a87a7-8120-49b2-91e6-7e2c9a95190e.xlsx"
        }

        response = requests.post(
            os.environ.get("URL_GET_FILE"),
            json=payload,
            headers=header
        )

        if response.status_code == 200:

            archive_in_memory = BytesIO(response.content)

            result = bancos[bank](archive_in_memory)

            output = BytesIO()
            result.to_excel(output, index=False)
            output.seek(0)

            if type(result) == str:
                return jsonify({"erro": result}), 400

            return send_file(
                response.content,
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                as_attachment=True,
                download_name="C6"
            )
            # requests.post(os.environ.get("URL_UPLOAD_FILE", ))

        else:
            return jsonify({"erro": f"Erro ao requisitar arquivo do banco {bank}"}), response.status_code

if __name__ == "__main__":
    app.run(debug=True)
