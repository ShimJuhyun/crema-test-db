from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import Integer, Boolean, String, DateTime, text
from sqlalchemy.dialects.postgresql import INET

class User(SQLModel, table=True):
    __tablename__ = "nice_user" # type: ignore

    id: str = Field(sa_column=Column(String(20), unique=True, nullable=False, primary_key=True))
    username: str = Field(sa_column=Column(String(20), unique=True, nullable=False))
    email: str = Field(sa_column=Column(String(255), unique=True, nullable=False))
    hashed_password: str = Field(sa_column=Column(String(255), nullable=False))
    ip_address: str = Field(sa_column=Column(INET, nullable=False))
    error_count: int = Field(default=0, sa_column=Column(Integer, nullable=False))
    is_active: bool = Field(default=True, sa_column=Column(Boolean, nullable=False, server_default="true"))
    user_level: int = Field(default=3, sa_column=Column(Integer, nullable=False, server_default=text("3")))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('now()')))
    updated_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()')))
