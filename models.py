from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_verified = Column(Boolean, default=False)
    failed_login_count = Column(Integer, default=0)
    lockout_until = Column(DateTime(timezone=True), nullable=True)
    refresh_jti = Column(String, nullable=True)

class Board(Base):
    __tablename__ = "boards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    position = Column(Integer, default=0)

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    board_id = Column(Integer, ForeignKey("boards.id", ondelete="CASCADE"), nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id", ondelete="SET NULL"), nullable=True)
    status_id = Column(Integer, nullable=True)
    position = Column(Integer, default=0)
