
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from sqlalchemy.orm import Session

from app.repositories import user_repo
from app.core.database import get_db
from app.services import user_service
from app.schemas.user_schema import User

import logging
logger = logging.getLogger(__name__)

# Router para futuras operaciones relacionadas con la gestión de usuarios
# (Ej: actualizar perfil, cambiar contraseña, etc.)
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/", response_class=JSONResponse)
async def read_users(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint de ejemplo para listar usuarios.
    En una implementación real, aquí se consultaría la base de datos y se devolverían los usuarios registrados.
    """
    logger.info("Endpoint /users/ accedido para listar usuarios")
    # Aquí se debería implementar la lógica para obtener los usuarios desde la base de datos
    users = user_repo.get_users(db)
    logger.info(f"Usuarios obtenidos: {len(users)}")

    
   
    # Devolvemos solo la información necesaria
    return [{"email": user.email} for user in users]
    
    #return "<h1>Lista de Usuarios</h1><p>{users}.</p>"

@router.post("/register", response_model=user_models.UserOut) # Definir un esquema de salida
async def register_user(
    user_data: user_models.UserCreate, # Recibimos el esquema de validación
    db: Session = Depends(get_db)
    ):    
    # Llamamos al servicio pasando los datos validados
    new_user = user.register_new_user(
        db, 
        email=user_data.email, 
        is_active=user_data.is_active, 
        gender=user_data.gender
    )
    logger.info(f"Usuario registrado con email: {new_user.email} ID: {new_user.id} API /users/register")
    return new_user

