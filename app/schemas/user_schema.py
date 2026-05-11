
# import enum

from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum as SqlEnum
from app.models.user_models import Gender

import logging
logger = logging.getLogger(__name__)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    height = Column(Integer, nullable=True)
    # Usamos el alias SqlEnum y pasamos la clase Gender
    # OJO: El default debe ser un miembro del Enum o None, no un string cualquiera
    gender = Column(SqlEnum(Gender), nullable=True)
