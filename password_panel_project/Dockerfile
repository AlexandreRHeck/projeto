# Usando uma imagem oficial do Python como base
FROM python:3.12

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar o arquivo de requisitos para o container
COPY requirements.txt .

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação para o container
COPY . .

# Expor a porta 8000 (porta padrão do Django)
EXPOSE 8000

# Comando para rodar o servidor Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
