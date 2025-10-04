# Conexión y configuración de la base de datos (MySQL con SQLAlchemy)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# URL de conexión a la base de datos (MySQL en este caso)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://si_user:si_pass@localhost:3306/si_db")

# Motor de conexión con pre_ping para reconectar si la conexión se cae
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

# Sesión para interactuar con la BD
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos
Base = declarative_base()

# Dependencia que nos da una sesión a la BD
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
