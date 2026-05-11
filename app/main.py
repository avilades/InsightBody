import logging
from pathlib import Path
import os
from fastapi import FastAPI
from .api.routers import user
from .services import user_service
from app.core.config_json import setup_logging, leer_config, initialize_lat_lon, initialize_logger_config
from .core.database import SessionLocal, engine
from .schemas import user_schema

# 1. Configurar el logging lo antes posible
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Insight Body API", 
    description="API para la gestión de usuarios y datos relacionados con el cuerpo humano", 
    version="1.0.0", contact={
    "name": "Equipo Insight Body",
    "email": "equipo@insightbody.com"
})

# --- Inclusión de Routers para organizar la API ---
app.include_router(user.router)     # Rutas de gestión de usuarios

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
user_schema.Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    #ejecutar_registro()
    logger.info("Aplicación iniciada correctamente. Listo para recibir solicitudes.")