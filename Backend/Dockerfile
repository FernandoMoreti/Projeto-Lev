# Usa uma imagem base leve do Python
FROM python:3.11-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências de sistema necessárias para o Pandas (se houver necessidade de compilação)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copia os arquivos de dependência e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código fonte para o container
COPY . .

# Expõe a porta que o Flask utilizará
EXPOSE 5000

ENV PYTHONPATH=/app

# Comando para rodar a aplicação
CMD ["python", "-m", "app.app", "--host=0.0.0.0"]