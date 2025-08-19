from datetime import datetime, timedelta, timezone
from typing import Tuple
import uuid, re, jwt
from passlib.context import CryptContext
from fastapi import Response
from settings import settings

SECRET_KEY = settings.SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def _token_payload(sub: str, jti: str, scope: str, expires_delta: timedelta):
    now = datetime.now(timezone.utc)
    exp = now + expires_delta
    return {"sub": sub, "jti": jti, "scope": scope, "iat": int(now.timestamp()), "exp": int(exp.timestamp())}

def create_access_token(user_id: int) -> Tuple[str, str]:
    jti = str(uuid.uuid4())
    payload = _token_payload(str(user_id), jti, "access", timedelta(minutes=settings.ACCESS_TOKEN_MINUTES))
    token = jwt.encode(payload, SECRET_KEY, algorithm=settings.JWT_ALG)
    return token, jti

def create_refresh_token(user_id: int) -> Tuple[str, str, int]:
    jti = str(uuid.uuid4())
    payload = _token_payload(str(user_id), jti, "refresh", timedelta(days=settings.REFRESH_TOKEN_DAYS))
    token = jwt.encode(payload, SECRET_KEY, algorithm=settings.JWT_ALG)
    return token, jti, payload["exp"]

def decode_token(token: str) -> dict:
    return jwt.decode(token, SECRET_KEY, algorithms=[settings.JWT_ALG])

def set_refresh_cookie(response: Response, refresh_token: str, exp_ts: int):
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        domain=settings.COOKIE_DOMAIN,
        expires=exp_ts,
        path="/auth/refresh",
    )

def clear_refresh_cookie(response: Response):
    response.delete_cookie("refresh_token", path="/auth/refresh", domain=settings.COOKIE_DOMAIN)

def password_policy_ok(pw: str) -> bool:
    if len(pw) < settings.PASSWORD_MIN_LENGTH: return False
    if " " in pw: return False
    if not re.search(r"[A-Z]", pw): return False
    if not re.search(r"[a-z]", pw): return False
    if not re.search(r"[0-9]", pw): return False
    return True
