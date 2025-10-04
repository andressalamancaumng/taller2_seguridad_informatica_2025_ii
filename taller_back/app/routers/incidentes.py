from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user, require_admin

# ✅ Todo el router requiere JWT
router = APIRouter(
    prefix="/incidentes",
    tags=["incidentes"],
    dependencies=[Depends(get_current_user)]
)

# --------------------------
# Obtener TODOS los incidentes
# --------------------------
@router.get("/", response_model=list[schemas.IncidenteRead])
def listar_incidentes(db: Session = Depends(get_db)):
    """
    Devuelve todos los incidentes registrados en el sistema.
    Requiere JWT válido.
    """
    return db.query(models.Incidente).all()

# --------------------------
# Obtener incidente por ID
# --------------------------
@router.get("/{incidente_id}", response_model=schemas.IncidenteRead)
def obtener_incidente(incidente_id: int, db: Session = Depends(get_db)):
    """
    Devuelve un incidente específico a partir de su ID.
    Requiere JWT válido.
    """
    incidente = db.query(models.Incidente).filter(models.Incidente.id == incidente_id).first()
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    return incidente

# --------------------------
# Crear incidente
# --------------------------
@router.post("/", response_model=schemas.IncidenteRead, status_code=201)
def crear_incidente(inc: schemas.IncidenteCreate, db: Session = Depends(get_db)):
    incidente = models.Incidente(titulo=inc.titulo, descripcion=inc.descripcion)
    if inc.estado:
        incidente.estado = models.EstadoIncidente(inc.estado)
    db.add(incidente)
    db.commit()
    db.refresh(incidente)
    return incidente

# --------------------------
# Actualizar incidente
# --------------------------
@router.put("/{incidente_id}", response_model=schemas.IncidenteRead)
def actualizar_incidente(incidente_id: int, inc: schemas.IncidenteUpdate, db: Session = Depends(get_db)):
    incidente = db.query(models.Incidente).filter(models.Incidente.id == incidente_id).first()
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    if inc.titulo is not None:
        incidente.titulo = inc.titulo
    if inc.descripcion is not None:
        incidente.descripcion = inc.descripcion
    if inc.estado is not None:
        incidente.estado = models.EstadoIncidente(inc.estado)
    db.commit()
    db.refresh(incidente)
    return incidente

# --------------------------
# Eliminar incidente (solo admin)
# --------------------------
@router.delete("/{incidente_id}", status_code=204, dependencies=[Depends(require_admin)])
def eliminar_incidente(incidente_id: int, db: Session = Depends(get_db)):
    incidente = db.query(models.Incidente).filter(models.Incidente.id == incidente_id).first()
    if not incidente:
        raise HTTPException(status_code=404, detail="Incidente no encontrado")
    db.delete(incidente)
    db.commit()
    return None
