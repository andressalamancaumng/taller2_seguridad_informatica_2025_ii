# Punto de entrada de la aplicación FastAPI

from fastapi import FastAPI
from .database import Base, engine
from . import models  # Asegura que los modelos se carguen

# Importa los routers directamente desde sus módulos
from .routers.users import router as users_router
from .routers.incidentes import router as incidentes_router

from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="Sistema Seguro (FastAPI + MySQL)")

# Crear tablas automáticamente si no existen
Base.metadata.create_all(bind=engine)

# Incluir rutas de usuarios e incidentes
app.include_router(users_router)
app.include_router(incidentes_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8100"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Ruta de salud (para saber si el servidor está corriendo)
@app.get("/health")
def health():
    return {"status": "ok"}
