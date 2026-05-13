
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from sqlalchemy.orm import Session

from app.repositories import user_repo
from app.core.database import get_db
from app.services import user_service
from app.models.user_models import UserCreate, UserOut

import logging
logger = logging.getLogger(__name__)

# Router para futuras operaciones relacionadas con la gestión de usuarios
# (Ej: actualizar perfil, cambiar contraseña, etc.)
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.get("/read_users", response_class=JSONResponse)
async def read_users(request: Request, db: Session = Depends(get_db)):
    """
    Endpoint de ejemplo para listar todos los usuarios.
    """
    logger.info("Endpoint /users/read accedido para listar usuarios")
    # Aquí se debería implementar la lógica para obtener los usuarios desde la base de datos
    users = user_repo.get_users(db)
    logger.info(f"Usuarios obtenidos: {len(users)}")

    # Devolvemos solo la información necesaria
    return [{"email": user.email, "is_active": user.is_active, "name": user.name, "surname": user.surname, "age": user.age, "height": user.height, "gender": user.gender} for user in users]

@router.get("/read_user/{email}", response_class=JSONResponse)
async def read_user(request: Request, db: Session = Depends(get_db), email: str = None):
    """
    Endpoint de ejemplo para listar un usuario específico por email.
    """
    logger.info("Endpoint /users/read_user accedido para listar un usuario específico")
    user = user_repo.get_user_by_email(db, email=email)
    
    logger.info(f"Usuarios encontrado: {len(user)}")

    # Devolvemos solo la información necesaria
    return [{"email": user.email, "is_active": user.is_active, "name": user.name, "surname": user.surname, "age": user.age, "height": user.height, "gender": user.gender} ]

# Definir un esquema de salida
@router.post("/register", response_model=UserOut)
async def register_user(
    user_data: UserCreate,  # Recibimos el esquema de validación
    db: Session = Depends(get_db)
):
    # Llamamos al servicio pasando los datos validados
    new_user = user_service.register_new_user(
        db,
        email=user_data.email,
        is_active=user_data.is_active,
        name=user_data.name,
        surname=user_data.surname,
        age=user_data.age,
        height=user_data.height,
        gender=user_data.gender
    )
    logger.info(
        f"Usuario registrado con email: {new_user.email} ID: {new_user.id} API /users/register")
    return new_user
    
