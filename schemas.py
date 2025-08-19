from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

# --- Auth ---
class RegisterIn(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8)

class RegisterOut(BaseModel):
    id: int
    email: EmailStr
    is_verified: bool

class LoginIn(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RefreshOut(BaseModel):
    access_token: str
    token_type: str = "bearer"

# --- Boards ---
class BoardBase(BaseModel):
    name: str
class BoardCreate(BoardBase): pass
class BoardUpdate(BaseModel):
    name: Optional[str] = None
class BoardOut(BoardBase):
    id: int

# --- Groups ---
class GroupBase(BaseModel):
    name: str
    board_id: int
    position: Optional[int] = 0
class GroupCreate(GroupBase): pass
class GroupUpdate(BaseModel):
    name: Optional[str] = None
    position: Optional[int] = None
class GroupOut(GroupBase):
    id: int

# --- Tasks ---
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    board_id: int
    group_id: Optional[int] = None
    status_id: Optional[int] = None
    position: Optional[int] = 0
class TaskCreate(TaskBase): pass
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    board_id: Optional[int] = None
    group_id: Optional[int] = None
    status_id: Optional[int] = None
    position: Optional[int] = None
class TaskMove(BaseModel):
    board_id: Optional[int] = None
    group_id: Optional[int] = None
    position: Optional[int] = None
class TaskOut(TaskBase):
    id: int

# --- Users (lectura) ---
class UserOut(BaseModel):
    id: int
    email: EmailStr
    is_verified: bool
    is_active: bool
