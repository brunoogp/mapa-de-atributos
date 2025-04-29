FROM python:3.10

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

# Instala as dependências
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expõe a porta da aplicação
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
