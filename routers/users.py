from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from deps import get_current_user
import models, schemas

router = APIRouter()

@router.get("/users/me", response_model=schemas.UserOut, summary="Usuario autenticado")
def me(user=Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "is_verified": user.is_verified, "is_active": user.is_active}

@router.get("/users/", response_model=List[schemas.UserOut], summary="Listar usuarios (demo)")
def list_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return [{"id": u.id, "email": u.email, "is_verified": u.is_verified, "is_active": u.is_active} for u in users]
