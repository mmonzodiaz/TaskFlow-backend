from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Body, Response, Request, status
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from security import (
    verify_password, hash_password,
    create_access_token, create_refresh_token,
    set_refresh_cookie, clear_refresh_cookie,
    password_policy_ok, decode_token
)
from settings import settings

router = APIRouter()

_failed_cache = {}

def _key(email: str, ip: str) -> str:
    return f"{email.lower()}|{ip}"

def _register_failure(email: str, ip: str):
    k = _key(email, ip)
    rec = _failed_cache.get(k, {"count": 0, "lock_until": 0})
    rec["count"] += 1
    if rec["count"] >= settings.MAX_FAILED_LOGINS:
        rec["lock_until"] = int(datetime.now(timezone.utc).timestamp()) + settings.LOCKOUT_MINUTES * 60
    _failed_cache[k] = rec

def _clear_failures(email: str, ip: str):
    _failed_cache.pop(_key(email, ip), None)

def _is_locked(email: str, ip: str):
    rec = _failed_cache.get(_key(email, ip))
    if not rec: return None
    now = int(datetime.now(timezone.utc).timestamp())
    if rec.get("lock_until", 0) > now:
        return rec["lock_until"]
    return None

@router.post("/auth/register", response_model=schemas.RegisterOut, summary="Registro con política de contraseña y hashing")
def register(payload: schemas.RegisterIn = Body(...), db: Session = Depends(get_db)):
    if not password_policy_ok(payload.password):
        raise HTTPException(status_code=400, detail="La contraseña no cumple la política mínima")
    existing = db.query(models.User).filter(models.User.email == payload.email.lower()).first()
    if existing:
        raise HTTPException(status_code=409, detail="El email ya está registrado")
    user = models.User(
        email=payload.email.lower(),
        hashed_password=hash_password(payload.password),
        is_active=True,
        is_verified=False,
    )
    db.add(user); db.commit(); db.refresh(user)
    return schemas.RegisterOut(id=user.id, email=user.email, is_verified=user.is_verified)

@router.post("/auth/login", response_model=schemas.TokenOut, summary="Login seguro con bloqueo por intentos y refresh cookie")
def login(response: Response, request: Request, payload: schemas.LoginIn = Body(...), db: Session = Depends(get_db)):
    ip = request.client.host if request.client else "unknown"
    until = _is_locked(payload.email, ip)
    if until:
        raise HTTPException(status_code=423, detail="Cuenta/IP temporalmente bloqueada por intentos fallidos")

    user = db.query(models.User).filter(models.User.email == payload.email.lower()).first()
    if not user or not verify_password(payload.password, user.hashed_password):
        _register_failure(payload.email, ip)
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Usuario inactivo")

    _clear_failures(payload.email, ip)

    access, access_jti = create_access_token(user.id)
    refresh, refresh_jti, refresh_exp = create_refresh_token(user.id)
    user.refresh_jti = refresh_jti
    db.commit()

    set_refresh_cookie(response, refresh, refresh_exp)
    return {"access_token": access, "token_type": "bearer"}

@router.post("/auth/refresh", response_model=schemas.RefreshOut, summary="Rotar refresh y obtener nuevo access")
def refresh_token(request: Request, response: Response, db: Session = Depends(get_db)):
    cookie = request.cookies.get("refresh_token")
    if not cookie:
        raise HTTPException(status_code=401, detail="Refresh token requerido")
    try:
        payload = decode_token(cookie)
    except Exception:
        raise HTTPException(status_code=401, detail="Refresh token inválido")
    if payload.get("scope") != "refresh":
        raise HTTPException(status_code=401, detail="Refresh token inválido")

    user_id = int(payload.get("sub"))
    jti = payload.get("jti")
    user = db.get(models.User, user_id)
    if not user or not user.is_active or user.refresh_jti != jti:
        raise HTTPException(status_code=401, detail="Refresh token no reconocido")

    access, _ = create_access_token(user.id)
    new_refresh, new_jti, new_exp = create_refresh_token(user.id)
    user.refresh_jti = new_jti
    db.commit()

    set_refresh_cookie(response, new_refresh, new_exp)
    return {"access_token": access, "token_type": "bearer"}

@router.post("/auth/logout", status_code=204, summary="Logout: invalidar refresh actual")
def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    cookie = request.cookies.get("refresh_token")
    if cookie:
        try:
            payload = decode_token(cookie)
            user_id = int(payload.get("sub"))
            user = db.get(models.User, user_id)
            if user:
                user.refresh_jti = None
                db.commit()
        except Exception:
            pass
    from security import clear_refresh_cookie
    clear_refresh_cookie(response)
    return None
