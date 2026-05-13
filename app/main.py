import logging
from pathlib import Path
import os
from fastapi import FastAPI, Request
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


def db_startup():
    # Docker inyecta las variables del .env directamente en el sistema
    POSTGRES_HOST = os.getenv('POSTGRES_HOST')
    POSTGRES_USER = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
    POSTGRES_PORT = os.getenv('POSTGRES_PORT')
    POSTGRES_DB = os.getenv('POSTGRES_DB')

    logger.info(f"Conectando a la base de datos con host: {POSTGRES_HOST}, user: {POSTGRES_USER}, port: {POSTGRES_PORT}, db: {POSTGRES_DB}")    
    # Crear las tablas
    user_schema.Base.metadata.create_all(bind=engine)


# --- Middleware de Logging de Peticiones ---
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Middleware global que intercepta cada petición HTTP para registrarla en el log.
    Captura: Método, Ruta, Dirección IP, Parámetros, Cuerpo, Código de estado y Tiempo de proceso.
    """
    import time
    start_time = time.time()
    
    # 1. Obtener información básica
    client_ip = request.client.host if request.client else "unknown"
    query_params = dict(request.query_params)
    
    # 2. Capturar el cuerpo de la petición de forma segura
    body = b""
    if request.method in ["POST", "PUT", "PATCH"]:
        body = await request.body()
        # Re-inyectamos el cuerpo en el canal de recepción para que FastAPI pueda leerlo después
        async def receive():
            return {"type": "http.request", "body": body}
        request._receive = receive

    # Loguear la petición entrante con todos sus detalles
    log_msg = f">>> Petición: {request.method} {request.url.path} | IP: {client_ip}"
    if query_params:
        log_msg += f" | QueryParams: {query_params}"
    if body:
        # Intentamos decodificar como texto, si falla lo dejamos como bytes truncados
        try:
            log_msg += f" | Body: {body.decode('utf-8')}"
        except:
            log_msg += f" | Body: <binary data: {len(body)} bytes>"
    
    logging.debug(log_msg)

    # 3. Procesar la petición
    response = await call_next(request)

    # 4. Información de la respuesta saliente
    process_time = time.time() - start_time
    logging.info(f"<<< Respuesta: {request.method} {request.url.path} - Status {response.status_code} - Tiempo: {process_time:.3f}s")
    
    return response

# --- Inclusión de Routers para organizar la API ---
app.include_router(user.router,  tags=["users"])     # Rutas de gestión de usuarios

@app.on_event("startup")
async def startup_event():
    logger.info("Evento de startup: Aplicación iniciada. Cargando configuración y preparando recursos...")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Evento de shutdown: Aplicación deteniéndose. Liberando recursos y cerrando conexiones...")

# Determinar la ruta de configuración relativa
current_dir = Path(__file__).resolve().parent
config_path = current_dir / "../config/config.json"

# 2. Leer los datos de configuración
config_data = leer_config(str(config_path))

if not config_data:
    logger.critical("No se pudo cargar la configuración. Deteniendo aplicación.")
    exit(1)

## # 3. Inicializar variables globales y re-configurar logging si es necesario
## LATITUD, LONGITUD = initialize_lat_lon(config_data)
#logger.info(f"Configuración de coordenadas inicializada. Coords: ({LATITUD}, {LONGITUD})")

db_startup()





if __name__ == "__main__":
    ## #ejecutar_registro()
    ## db_startup()
    logger.info(" --------- Aplicación iniciada. Listo para recibir peticiones. ------")