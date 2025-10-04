# Rutas de usuarios: registro, login, info de usuario, endpoint solo para admin

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, Field
from fastapi.security import OAuth2PasswordRequestForm

from .. import models, schemas
from ..database import get_db
from ..auth import hash_password, verify_password, create_access_token, get_current_user, require_admin

router = APIRouter(tags=["usuarios"])

@router.post("/register", response_model=schemas.UserRead, status_code=201)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """Registrar un nuevo usuario (admin o normal)"""
    exists = db.query(models.User).filter(models.User.email == user_in.email).first()
    if exists:
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    user = models.User(
        email=user_in.email,
        password_hash=hash_password(user_in.password),
        rol=models.RolEnum(user_in.rol) if user_in.rol in ("admin","usuario") else models.RolEnum.usuario
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

@router.post("/login", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login: devuelve un JWT si las credenciales son correctas"""
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")
    token = create_access_token({"sub": str(user.id), "email": user.email, "rol": user.rol.value})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/me", response_model=schemas.UserRead)
def me(current_user: models.User = Depends(get_current_user)):
    """Devuelve la información del usuario autenticado"""
    return current_user

@router.get("/admin/ping")
def admin_ping(_: models.User = Depends(require_admin)):
    """Ejemplo de endpoint restringido a admin"""
    return {"ok": True, "msg": "Hola, admin"}

# --------------------------
# Esquema para actualizar usuario
# --------------------------
class UserUpdate(BaseModel):
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)

# --------------------------
# Editar el propio usuario
# --------------------------
@router.put("/me", response_model=schemas.UserRead)
def update_me(
    update: UserUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """
    Permite que el usuario autenticado edite su propio perfil.
    Puede cambiar correo y/o contraseña.
    Requiere JWT válido.
    """
    user = db.query(models.User).filter(models.User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    # Actualizar correo si viene
    if update.email:
        existe = db.query(models.User).filter(models.User.email == update.email).first()
        if existe and existe.id != current_user.id:
            raise HTTPException(status_code=400, detail="Ese correo ya está en uso")
        user.email = update.email

    # Actualizar contraseña si viene
    if update.password:
        user.password_hash = hash_password(update.password)

    db.commit()
    db.refresh(user)
    return user