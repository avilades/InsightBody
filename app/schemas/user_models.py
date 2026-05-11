
import enum

from app.core.database import Base
from sqlalchemy import Column, Integer, String, Boolean, Enum as SqlEnum

class Gender(enum.Enum):
    valor1 = "mujer"
    valor2 = "hombre"
    valor3 = "otro"

class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    is_active = Column(Boolean, default=True)
    # Usamos el alias SqlEnum y pasamos la clase Gender
    # OJO: El default debe ser un miembro del Enum o None, no un string cualquiera
    gender = Column(SqlEnum(Gender), nullable=True)