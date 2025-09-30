from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from .models import bancos
from io import BytesIO
from datetime import datetime


app = Flask(__name__) #cria o app, inicializa a aplicação flask
CORS(app, origins=["https://projeto-lev.vercel.app"], expose_headers=["Content-Disposition"])

@app.route("/executar", methods=["POST"])
def executar():
    nome_banco = request.form.get("banco")
    arquivo = request.files.get("arquivo")
    nome_banco = nome_banco.lower()

    if nome_banco not in bancos:
        return jsonify({"erro": "Função não encontrada"}), 400
    
    if not arquivo:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    resultado = bancos[nome_banco](arquivo)

    output = BytesIO()
    resultado.to_excel(output, index=False)
    output.seek(0)

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

if __name__ == "__main__":
    app.run(debug=True)
