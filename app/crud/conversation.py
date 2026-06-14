from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.conversation import Conversation, Message, MessageRole


async def create_conversation(
    session: AsyncSession, user_id: UUID, title: str | None = None
) -> Conversation:
    conversation = Conversation(user_id=user_id, title=title)
    session.add(conversation)
    await session.commit()
    await session.refresh(conversation)
    return conversation


async def get_conversation(session: AsyncSession, conversation_id: UUID) -> Conversation | None:
    result = await session.execute(
        select(Conversation)
        .where(Conversation.id == conversation_id)
        .options(selectinload(Conversation.messages))
    )
    return result.scalar_one_or_none()


async def list_conversations(session: AsyncSession, user_id: UUID) -> list[Conversation]:
    result = await session.execute(
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.created_at.desc())
    )
    return result.scalars().all()


async def add_message(
    session: AsyncSession,
    conversation_id: UUID,
    role: MessageRole,
    content: str,
    tool_calls: dict | None = None,
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        tool_calls=tool_calls,
    )
    session.add(message)
    await session.commit()
    await session.refresh(message)
    return message


async def get_conversation_messages(
    session: AsyncSession, conversation_id: UUID
) -> list[Message]:
    result = await session.execute(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc())
    )
    return result.scalars().all()
