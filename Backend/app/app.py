from flask import Flask, request, jsonify
from models import bancos

app = Flask(__name__) #cria o app, inicializa a aplicação flask

@app.route("/executar", methods=["POST"])
def executar():
    nome_banco = request.form.get("banco")
    arquivo = request.files.get("arquivo")

    if nome_banco not in bancos:
        return jsonify({"erro": "Função não encontrada"}), 400
    
    if not arquivo:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    resultado = bancos[nome_banco](arquivo)

    return jsonify({"resultado": resultado})

if __name__ == "__main__":
    app.run(debug=True)
