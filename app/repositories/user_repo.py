from sqlalchemy.orm import Session
from app.schemas import user_models

def get_usuario_by_email(db: Session, email: str):
    return db.query(user_models.Usuario).filter(user_models.Usuario.email == email).first()

def crear_usuario(db: Session, email: str, gender: user_models.Gender):
    db_user = user_models.Usuario(email=email, is_active=True, gender=gender)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user