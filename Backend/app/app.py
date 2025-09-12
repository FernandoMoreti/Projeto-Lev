from flask import Flask, request, jsonify
from flask_cors import CORS
from models import bancos

app = Flask(__name__) #cria o app, inicializa a aplicação flask
CORS(app)

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

    return jsonify({"resultado": resultado}), 200

if __name__ == "__main__":
    app.run(debug=True)
