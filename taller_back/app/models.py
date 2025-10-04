# Definición de las tablas en SQLAlchemy (Usuarios e Incidentes)

from sqlalchemy import Column, Integer, String, Enum, DateTime, Text
from sqlalchemy.sql import func
import enum
from .database import Base

# Enumeración para roles de usuario
class RolEnum(str, enum.Enum):
    admin = "admin"
    usuario = "usuario"

# Enumeración para estados de los incidentes
class EstadoIncidente(str, enum.Enum):
    ABIERTO = "ABIERTO"
    EN_PROCESO = "EN_PROCESO"
    CERRADO = "CERRADO"

# Tabla de usuarios
class User(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True, index=True)  # Identificador único
    email = Column(String(255), unique=True, nullable=False, index=True)  # Correo único
    password_hash = Column(String(255), nullable=False)  # Contraseña cifrada con bcrypt
    rol = Column(Enum(RolEnum), default=RolEnum.usuario, nullable=False)  # Rol (admin/usuario)

# Tabla de incidentes
class Incidente(Base):
    __tablename__ = "incidentes"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), nullable=False)  # Título del incidente
    descripcion = Column(Text, nullable=True)  # Detalles
    estado = Column(Enum(EstadoIncidente), default=EstadoIncidente.ABIERTO, nullable=False)
    creado_en = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)  # Fecha de creación
    actualizado_en = Column(DateTime(timezone=True), onupdate=func.now())  # Fecha de última actualización
