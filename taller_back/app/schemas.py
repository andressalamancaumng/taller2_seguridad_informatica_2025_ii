# Esquemas (modelos de datos) para validar entradas y salidas en la API

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# --- Usuarios ---

# Esquema para crear usuario (entrada)
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)  # Validamos mínimo 8 caracteres
    rol: Optional[str] = "usuario"

# Esquema para devolver usuario (salida)
class UserRead(BaseModel):
    id: int
    email: EmailStr
    rol: str
    class Config:
        from_attributes = True  # Permite leer directamente desde SQLAlchemy

# --- Autenticación ---

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"  # Tipo de token (JWT Bearer)

class TokenData(BaseModel):
    user_id: int
    email: EmailStr
    rol: str

# --- Incidentes ---

# Base común
class IncidenteBase(BaseModel):
    titulo: str
    descripcion: Optional[str] = None
    estado: Optional[str] = None

# Para crear incidente
class IncidenteCreate(IncidenteBase):
    pass

# Para actualizar incidente
class IncidenteUpdate(BaseModel):
    titulo: Optional[str] = None
    descripcion: Optional[str] = None
    estado: Optional[str] = None

# Para devolver incidente completo
class IncidenteRead(BaseModel):
    id: int
    titulo: str
    descripcion: Optional[str]
    estado: str
    creado_en: datetime
    actualizado_en: Optional[datetime]
    class Config:
        from_attributes = True
