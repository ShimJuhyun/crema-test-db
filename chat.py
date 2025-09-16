from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import String, Column

from database import DEFAULT_MAX_KEY_LENGTH, DEFAULT_MAX_VARCHAR_LENGTH

class Chat(SQLModel, table=True):
    __tablename__ = "nice_chat" 

    id: str = Field(sa_column=Column(String(DEFAULT_MAX_KEY_LENGTH), unique=True, nullable=False, primary_key=True))
    title: str = Field(sa_column=Column(String(DEFAULT_MAX_VARCHAR_LENGTH), nullable=True))