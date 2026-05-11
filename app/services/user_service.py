from app.api.routers import user
from app.repositories import user_repo as crud

from sqlalchemy.orm import Session
from app.schemas.user_schema import User
from app.models.user_models import UserCreate

import logging
logger = logging.getLogger(__name__)

def register_new_user(db: Session, email: str, is_active: bool, gender):
    # Lógica de negocio: Verificar si existe antes de crear
    existente = crud.get_user_by_email(db, email)
    if existente:
        raise Exception("El usuario ya existe")
    
    # 1. Crear la instancia del modelo de SQLAlchemy
    db_user = User(
        email=email,
        is_active=is_active,
        gender=gender
    )
    
    # 2. Agregar a la sesión y confirmar (commit)
    db.add(db_user)
    db.commit()

    # Lógica extra: Enviar email (pseudocódigo)
    # email_service.send_welcome(email)
    logger.info(f"Usuario registrado: {email} - Servicio user_service")
    return  db_user