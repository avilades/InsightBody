"""
Archivo de carga de configuraciones
Aqui almacenamos en variables globales las configuraciones del archivo config.json
Que luego se usan en el resto de la aplicacion, al importar este archivo
"""
import logging
import json
import os
from pathlib import Path
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

logger = logging.getLogger(__name__)


def leer_config(config_file=None):
    """
    Función para leer el archivo de configuración completo.

    Parámetros:
    - config_file: Ruta al archivo de configuración. Si es None, se usa la ruta por defecto.

    Retorna:
    - config_data: Diccionario con los datos del archivo de configuración.
    """
    if config_file is None:
        # 1. Obtenemos la ruta de 'config_json.py'
        current_path = Path(__file__).resolve()
        # 2. Subimos dos niveles (a la raíz del proyecto) y bajamos a 'config/config.json'
        config_file = current_path.parent.parent.parent / "config" / "config.json"
    else:
        config_file = Path(config_file)

    logger.info(f"Ruta del archivo de configuración: {config_file}")
    
    try:
        # 3. Leemos el archivo
        with open(config_file, "r", encoding="utf-8") as j:
            config_data = json.load(j)
            logger.info("Archivo de configuración leído correctamente")
            return config_data
    except Exception as e:
        logger.error(f"Error al leer el archivo de configuración: {e}")
        return None


def initialize_lat_lon(config_data=None):
    """
    Inicializa las variables globales de latitud y longitud.
    """
    global LATITUD, LONGITUD
    
    config_json_data = config_data
    
    LATITUD = config_json_data.get("latitud")
    LONGITUD = config_json_data.get("longitud")

    logger.info(f"Variables de latitud y longitud inicializadas Latitud: {LATITUD}, Longitud: {LONGITUD}")

    return LATITUD, LONGITUD


def initialize_logger_config(config_data=None):
    """
    Inicializa las variables globales relacionadas con la configuración del logger.
    """
    global LOG_LEVEL, LOG_DIR, LOG_FILE_NAME, BACKUP_COUNT, LOG_FORMAT
    
    if config_data is None:
        config_data = leer_config()
    
    if config_data is None:
        # Valores por defecto si no hay config_data
        LOG_LEVEL = "INFO"
        LOG_DIR = "logs"
        LOG_FILE_NAME = "app.log"
        BACKUP_COUNT = 30
        LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    else:
        log_config = config_data.get("log_config", {})
        LOG_LEVEL = log_config.get("log_level", "INFO")
        LOG_DIR = log_config.get("log_dir", "logs")
        LOG_FILE_NAME = log_config.get("log_file_name", "app.log")
        BACKUP_COUNT = log_config.get("backup_count", 30)
        LOG_FORMAT = log_config.get("log_format", "%(asctime)s - %(levelname)s - %(message)s")

    return LOG_LEVEL, LOG_DIR, LOG_FILE_NAME, BACKUP_COUNT, LOG_FORMAT

def setup_logging(config_data=None):
    """
    Configura el registro de logs con rotación diaria.
    Los logs se almacenan en el directorio 'logs' con el formato LOG_FILE_NAME_YYYYMMDD.log.
    """
    global LOG_LEVEL, LOG_DIR, LOG_FILE_NAME, BACKUP_COUNT, LOG_FORMAT

    # Si no se pasan datos, intentamos inicializar con los globales o cargar el archivo
    if config_data is not None or LOG_FILE_NAME is None:
        initialize_logger_config(config_data)

    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    # Nombre base del archivo de log
    log_base = os.path.join(LOG_DIR, LOG_FILE_NAME)

    handler = TimedRotatingFileHandler(
        log_base,
        when="midnight",
        interval=1,
        backupCount=BACKUP_COUNT,
        encoding="utf-8"
    )

    handler.suffix = "%Y%m%d"

    def namer(default_name):
        if ".log." in default_name:
            parts = default_name.split(".log.")
            return f"{parts[0]}_{parts[1]}.log"
        return default_name

    handler.namer = namer

    # Configuración global del logger raíz
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL.upper(), logging.INFO),
        format=LOG_FORMAT,
        #StreamHandler para que también se vea en consola, útil para desarrollo y Docker logs
        #handlers=[handler, logging.StreamHandler()],
        handlers=[handler],
        force=True
    )
    
    logging.info("Sistema de logs inicializado.")
    logging.info(f"Archivo: {log_base} -- Log level: {LOG_LEVEL}")

# Inicializamos las variables globales al importar el módulo
LATITUD, LONGITUD = None, None
LOG_LEVEL, LOG_DIR, LOG_FILE_NAME, BACKUP_COUNT, LOG_FORMAT = None, None, None, None, None

if __name__ == "__main__":
    # 1. Obtenemos la ruta de 'config_json.py'
    current_path = Path(__file__).resolve()
    # 2. Subimos un nivel (a 'app/') y bajamos a 'config/config.json'
    config_file = current_path.parent.parent / "config" / "config.json"
    # 3. Leemos el archivo
    config_data = leer_config(str(config_file))

    initialize_lat_lon(config_data)
    initialize_logger_config(config_data)
    logger.info(f"Configuración del logger inicializada. LOG_LEVEL: {LOG_LEVEL}, LOG_DIR: {LOG_DIR}, LOG_FILE_NAME: {LOG_FILE_NAME}")
 
