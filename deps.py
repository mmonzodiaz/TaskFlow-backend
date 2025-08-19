from fastapi import Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
import jwt
from database import get_db
import models
from settings import settings

SECRET_KEY = settings.SECRET_KEY

def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.User:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales requeridas")
    token = auth.split(" ", 1)[1]
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[settings.JWT_ALG])
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    if payload.get("scope") != "access":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token inválido")
    user_id = int(payload.get("sub"))
    user = db.get(models.User, user_id)
    if not user or not user.is_active:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario inactivo o no encontrado")
    return user
