# Usamos una versión ligera de Python 3.11
FROM mcr.microsoft.com/vscode/devcontainers/python:3.11

# Evita que Python genere archivos .pyc y permite ver logs en tiempo real
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Instalamos dependencias del sistema necesarias para conectarse a Postgres (psycopg2)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# (Opcional) Instalar tus librerías si tienes un requirements.txt
COPY requirements.txt .
RUN pip install -r requirements.txt