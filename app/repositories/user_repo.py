from sqlalchemy.orm import Session
from app.schemas.user_schema import User
from app.models.user_models import Gender

import logging
logger = logging.getLogger(__name__)


def get_user_by_email(db: Session, email: str):
    user_by_email = db.query(
        User,
        User.email,
        User.is_active,
        User.name,
        User.surname,
        User.age,
        User.height,
        User.gender
    ).filter(User.email == email).first()
    logger.info(f"Usuario obtenido por email: {email}")
    return user_by_email


def create_user(
            db: Session,
            email: str,
            is_active: bool,
            name: str,
            surname: str,
            age: int | None,
            height: int | None,
            gender: Gender
        ):
    db_user = User.User(
            email=email,
            is_active=is_active,
            name=name,
            surname=surname,
            age=age,
            height=height,
            gender=gender
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    logger.info(
        f"Usuario creado en DB: {email} con género: {gender} repositorio user_repo")
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 100):
    users = db.query(
        User
    ).offset(skip).limit(limit).all()
    logger.info(f"Usuarios obtenidos: {len(users)} desde repositorio user_repo, get_users")
    return users
