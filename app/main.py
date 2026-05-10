
import os
import psycopg2 # Necesitarás instalar 'psycopg2-binary'

import logging
from venv import logger

from app.logging_config import setup_logging

# Inicializamos el sistema de logs
setup_logging()

logger = logging.getLogger(__name__)




# Docker inyecta las variables del .env directamente en el sistema
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

logger.info(f"Intentando conectar a PostgreSQL en {POSTGRES_HOST}:{POSTGRES_PORT} con usuario {POSTGRES_USER}")

try:
    conn = psycopg2.connect(
        dbname=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD,
        host=POSTGRES_HOST,
        port=POSTGRES_PORT
    )
    print("¡Conexión exitosa a PostgreSQL!")
    logger.info("Conexión exitosa a PostgreSQL")
    conn.close()
except Exception as e:
    print(f"Error al conectar: {e}")
    logger.error(f"Error al conectar a PostgreSQL: {e}")