from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String, Text, DateTime, Boolean, ForeignKey, text
from sqlalchemy.dialects.postgresql import INET

class RefreshToken(SQLModel, table=True):
    __tablename__ = "nice_refresh_tokens" # type: ignore

    user_id: str = Field(sa_column=Column(String(20), ForeignKey("nice_user.id", ondelete="CASCADE"), nullable=False, primary_key=True))
    token: str = Field(sa_column=Column(Text, unique=True, nullable=False, primary_key=True))
    created_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('now()')))
    expires_at: datetime = Field(sa_column=Column(DateTime(timezone=True), nullable=False))
    revoked: bool = Field(default=False, sa_column=Column(Boolean, nullable=False, server_default="false"))
    replace_by_token: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
    ip_address: str = Field(sa_column=Column(INET, nullable=False))
    user_agent: Optional[str] = Field(default=None, sa_column=Column(Text, nullable=True))
