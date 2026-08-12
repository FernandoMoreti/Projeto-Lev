<h1>🚀 Projeto Fastex</h1>
<h3>Nova automação na área</h3>

<hr>

<h2>📌 Visão Geral</h2>
<p>
O <strong>Projeto Fastex</strong> é uma aplicação desenvolvida para realizar a
<strong>edição e conversão automatizada de relatórios</strong> nos formatos
Excel, CSV, PDF e TXT para um modelo padrão de Excel <strong>Workbank</strong>.
</p>

<h3>Descrição</h3>

<p>
O projeto tem como principal objetivo reduzir o trabalho manual do setor de comissao,
responsável pela edição desses relatórios, garantindo padronização, agilidade
e confiabilidade no processamento das informações.
</p>

<h3>Status</h3>

<p>O projeto atualmente se encontra em: Produção</p>

<h3>Tecnologias utilizadas</h3>

<p>Backend: Python, Flask, CORS, pandas, base64</p>
<p>Observabilidade: logger</p>
<p>DevOps: Docker</p>

<h2>Pré-requisitos</h2>

<p>Python</p>

<hr>

<h2>Problema Resolvido</h2>
<p>
A edição manual de relatórios é um processo demorado e sujeito a erros.
O Projeto Fastex automatiza esse fluxo, convertendo relatórios brutos
em um formato compatível com o sistema do Workbank.
</p>

<hr>

<h2>🎯 Público-Alvo</h2>
<p>Integrantes do <strong>time de comissão</strong>.</p>

<hr>

<h2>🎯 Objetivos</h2>

<h3>Objetivo Geral</h3>
<p>
Editar automaticamente relatórios de comissão
extraídos do banco convertendo-os para um modelo compatível com o sistema Workbank.
</p>

<h3>Objetivos Específicos</h3>
<ul>
  <li>Ler arquivos retirados do banco</li>
  <li>Editar esses arquivos conforme regras definidas</li>
  <li>Converter os dados para um excel no modelo padrão Workbank</li>
  <li>Enviar uma lista das propostas como resposta juntamente com o arquivo editado e padronizado para download</li>
</ul>

<hr>

<h2>⚙️ Funcionalidades</h2>
<ul>
  <li>Leitura de arquivos em diferentes formatos</li>
  <li>Edição automática de relatórios</li>
  <li>Conversão para o modelo Workbank</li>
  <li>Retornar uma lista com todas as propostas editadas</li>
  <li>Download automático do arquivo editado</li>
</ul>

<hr>

<h2>✅ Validações Importantes</h2>
<ul>
  <li>Validação de dados recebidos, conferindo existencia de dados obrigatórios</li>
  <li>Validação do dados gerados, conferindo existencia de valores obrigatórios</li>
  <li>Validação do modelo final para garantir compatibilidade com o Workbank</li>
  <li>Verificação se a edição atende a todos os critérios de leitura do sistema</li>
</ul>

<hr>

<h2>🏗️ Arquitetura e Estrutura do Projeto</h2>

<h3>Backend</h3>
<pre>
backend/
 ├── app/
 |   ├── models/
 |   |   └── TODOS OS ARQUIVOS DOS BANCOS
 |   ├── utils.py
 |   ├── logger.py
 |   ├── mapper.py
 |   └── app.py
 ├── logs/
 └── temp/
</pre>

<hr>

<h2>▶️ Como Executar o Projeto</h2>

<h3>Terminal code</h3>
<pre>
  pip install -r requirements.txt
  python -m app.app
</pre>

<h3>Terminal Docker</h3>
<pre>
  docker-compose up -d --build
</pre>

<p>Após esses passos, a aplicação estará rodando localmente.</p>

<hr>

<h2>👤 Como Usar (Usuário Final)</h2>
<ol>
  <li>Acessar a aplicação desenvolvida pelo time responsavel</li>
  <li>Faça uma request com o metodo post no endpoint "/execute" com o seguinte body no formato de FormData:
    {
      "banco": "exemplo",
      "arquivo": exemplo.xlsx
    }
  </li>
  <li>O retorno sera enviado da seguinte forma para capitação do Front:
  {
    "mensagem": "Sucesso",
    "nome_arquivo": nome_arquivo,
    "arquivo_base64": excel_base64,
    "listOfProposal": listOfProposal
  }
  </li>
</ol>

<hr>

<h2>🔄 Fluxo do Sistema</h2>
<ol>
  <li>O usuário envia o arquivo e seleciona o banco</li>
  <li>O frontend encaminha os dados para o backend</li>
  <li>O backend identifica o banco e aplica a edição correta</li>
  <li>O arquivo convertido é retornado ao frontend</li>
  <li>O download é iniciado automaticamente</li>
</ol>

<hr>

<h2>⚠️ Limitações Conhecidas</h2>
<ul>
  <li>Alguns bancos ainda não possuem um padrão definido de arquivos</li>
  <li>Esses formatos precisam ser parametrizados para edição correta</li>
</ul>

<hr>

<h2>🧱 Pontos Fracos Atuais</h2>
<ul>
  <li>Para adicionar um novo banco o processo é totalmente manual de capitação de campos</li>
</ul>

<hr>

<h2>🛠️ Ajustes Desejados</h2>
<ul>
  <li>Reestruturação das pastas para um modelo mais profissional</li>
  <li>Evolução da arquitetura do projeto</li>
</ul>

<hr>

<h2>🔗 Links Importantes</h2>
<ul>
  <li>
    <strong>Repositório:</strong>
    <a href="https://github.com/FernandoMoreti/Projeto-Lev" target="_blank">
      https://github.com/FernandoMoreti/Projeto-Lev
    </a>
  </li>
  <li>
    <strong>Aplicação em produção:</strong>
    <a href="http://192.168.1.90/5000" target="_blank">
      http://192.168.1.90/5000
    </a>
  </li>
</ul>

<hr>

<h2>📄 Licença</h2>
<p>Uso interno — LEV Negócios</p>
<h2>Desenvolvido por:</h2>
<p>Fernando Moreti Bolela e Silva</p>

