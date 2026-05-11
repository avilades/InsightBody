from sqlalchemy.orm import Session
from app.schemas import user_schema

import logging
logger = logging.getLogger(__name__)


def get_user_by_email(db: Session, email: str):
    user_by_email = db.query(user_schema.User).filter(user_schema.User.email == email).first()
    logger.info(f"Usuario obtenido por email: {email}")
    return user_by_email

def create_user(db: Session, email: str, gender: user_schema.Gender):
    db_user = user_schema.User(email=email, is_active=True, gender=gender)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(f"Usuario creado en DB: {email} con género: {gender} repositorio user_repo")
    return db_user

def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(user_schema.User).offset(skip).limit(limit).all()
    logger.info(f"Usuarios obtenidos: {len(users)}")
    return users