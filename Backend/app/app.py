from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from .models import bancos
from io import BytesIO
from datetime import datetime


app = Flask(__name__) #cria o app, inicializa a aplicação flask 
CORS(app, origins=["https://projeto-lev.vercel.app", "http://localhost:5173"], expose_headers=["Content-Disposition"])

@app.route("/executar", methods=["POST"])
def executar():

    col_opcoes = [
        "NUM_BANCO",
        "NOM_BANCO",
        "NUM_PROPOSTA",
        "NUM_CONTRATO",
        "NOM_CLIENTE",
        "COD_CPF_CLIENTE",
        "DSC_PRODUTO",
        "DSC_SITUACAO_BANCO",
        "DSC_OBSERVACAO",
        "DAT_CREDITO",
        "VAL_BRUTO",
        "VAL_LIQUIDO",
        "VAL_SALDO_REFINANCIAMENTO",
        "VAL_BASE_COMISSAO",
        "VAL_COMISSAO",
        "PCL_COMISSAO",
        "DSC_TIPO_COMISSAO",
        "COD_LOJA",
        "COD_UNIDADE_EMPRESA",
        "COD_BANCO",
        "COD_TIPO_PROPOSTA_EMPRESTIMO",
        "DSC_TIPO_PROPOSTA_EMPRESTIMO",
        "NIC_CTR_USUARIO",
        "COD_PRODUTO",
        "COD_PRODUTOR_VENDA",
        "COD_PRODUTOR_VENDA_BANCO",
        "COD_TIPO_COMISSAO",
        "COD_SITUACAO_EMPRESTIMO",
        "QTD_PARCELA",
        "NUM_PARCELA_DIFERIDA_EMPRESA",
        "DAT_EMPRESTIMO",
        "DAT_CONFIRMACAO",
        "DAT_ESTORNO",
        "DAT_CTR_INCLUSAO",
        "TIPO_COMISSAO_BANCO",
        "PCL_TAXA_EMPRESTIMO"
    ]

    nome_banco = request.form.get("banco")
    arquivo = request.files.get("arquivo")
    nome_banco = nome_banco.lower()

    print(f"Banco selecionado: {nome_banco}")
    print(f"Arquivo recebido: {arquivo.filename if arquivo else 'Nenhum arquivo'}")
    
    if nome_banco not in bancos:
        return jsonify({"erro": "Função não encontrada"}), 400
    
    if not arquivo:
        return jsonify({"erro": "Nenhum arquivo enviado"}), 400
    
    resultado = bancos[nome_banco](arquivo, col_opcoes)

    print("Log do resultado:" )
    print(resultado)

    if type(resultado) is str:
        return jsonify({"erro": resultado}), 400

    output = BytesIO()
    resultado.to_excel(output, index=False)
    output.seek(0)
    nome_banco = nome_banco.upper()

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
