import logging
from pathlib import Path
import os
from fastapi import FastAPI
from .services import user_service
from app.core.config_json import setup_logging, leer_config, initialize_lat_lon, initialize_logger_config
from .core.database import SessionLocal, engine
from .schemas import user_models

# 1. Configurar el logging lo antes posible
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI()

logger.info("--- Iniciando carga de configuración global ---")

# Determinar la ruta de configuración relativa
current_dir = Path(__file__).resolve().parent
config_path = current_dir / "../config/config.json"

# 2. Leer los datos de configuración
config_data = leer_config(str(config_path))

if not config_data:
    logger.critical("No se pudo cargar la configuración. Deteniendo aplicación.")
    exit(1)

# 3. Inicializar variables globales y re-configurar logging si es necesario
LATITUD, LONGITUD = initialize_lat_lon(config_data)
setup_logging(config_data)

logger.info(f"Configuración de coordenadas inicializada. Coords: ({LATITUD}, {LONGITUD})")

# Docker inyecta las variables del .env directamente en el sistema
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')

logger.info(f"Conectando a la base de datos con host: {POSTGRES_HOST}, user: {POSTGRES_USER}, port: {POSTGRES_PORT}, db: {POSTGRES_DB}")    
# Crear las tablas
user_models.Base.metadata.create_all(bind=engine)

def ejecutar_registro():
    db = SessionLocal()
    try:
        nuevo = user_service.registrar_nuevo_usuario(db, "test_5@ejemplo.com", gender=user_models.Gender.valor1)
        logger.info(f"Usuario creado: {nuevo.id}")
    finally:
        db.close()

if __name__ == "__main__":
    ejecutar_registro()