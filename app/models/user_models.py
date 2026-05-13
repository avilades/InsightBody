from pydantic import BaseModel, EmailStr

import enum

import logging
logger = logging.getLogger(__name__)


class Gender(enum.Enum):
    valor1 = "mujer"
    valor2 = "hombre"
    valor3 = "otro"

class UserCreate(BaseModel):
    email: EmailStr
    is_active: bool
    name: str
    surname: str
    age: int | None = None
    height: int | None = None
    gender: Gender

class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_active: bool
    name: str
    surname: str
    age: int | None = None
    height: int | None = None
    gender: Gender

    class Config:
        from_attributes = True # Esto es vital en Pydantic v2 (u orm_mode = True en v1)