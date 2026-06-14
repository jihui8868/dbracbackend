from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[UUID] = None


class MessageResponse(BaseModel):
    id: UUID
    role: str
    content: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationResponse(BaseModel):
    id: UUID
    title: Optional[str]
    created_at: datetime
    messages: list[MessageResponse] = []

    class Config:
        from_attributes = True


class ChatStreamChunk(BaseModel):
    type: str
    content: str
