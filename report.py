import uuid
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String, DateTime, text, ForeignKey, TEXT, BigInteger
from sqlalchemy.dialects.postgresql import UUID

from database import DEFAULT_MAX_KEY_LENGTH, DEFAULT_MAX_VARCHAR_LENGTH

class ReportArchive(SQLModel, table=True):
   __tablename__ = "nice_report_archive"

   report_seq: Optional[int] = Field(sa_column=Column(BigInteger, autoincrement=True, primary_key=True, nullable=False))
   report_id: Optional[uuid.UUID] = Field(sa_column=Column(UUID(as_uuid=True), server_default=text("gen_random_uuid()"), primary_key=True, nullable=False))
   report_type: str = Field(sa_column=Column(String(10), nullable=False))
   agent_id: Optional[str] = Field(sa_column=Column(String(20), primary_key=True))
   chat_id: Optional[str] = Field(sa_column=Column(String(DEFAULT_MAX_KEY_LENGTH), ForeignKey("nice_chat.id"), nullable=True))
   message_id: Optional[str] = Field(sa_column=Column(String(DEFAULT_MAX_KEY_LENGTH), nullable=True))
   report_title: str = Field(sa_column=Column(String(DEFAULT_MAX_VARCHAR_LENGTH)))
   description: str = Field(sa_column=Column(TEXT))
   report_content: str = Field(sa_column=Column(TEXT))
   user_id: str = Field(sa_column=Column(String(20), nullable=False))
   created_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('now()')))
   updated_at: Optional[datetime] = Field(sa_column=Column(DateTime(timezone=True), nullable=False, server_default=text('now()'), onupdate=text('now()')))