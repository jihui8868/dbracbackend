import json
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.user import UserResponse
from app.schemas.chat import ChatRequest, ConversationResponse
from app.crud.conversation import (
    create_conversation,
    get_conversation,
    list_conversations,
    add_message,
    get_conversation_messages,
)
from app.models.conversation import MessageRole
from app.router.auth import get_current_user
from app.agents.main_agent import agent

router = APIRouter()


@router.get("/sessions")
async def list_sessions(
    current_user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    conversations = await list_conversations(session, current_user.id)
    return [
        {
            "id": str(conv.id),
            "title": conv.title,
            "created_at": conv.created_at,
        }
        for conv in conversations
    ]


@router.post("/sessions")
async def create_session(
    current_user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    conversation = await create_conversation(session, current_user.id)
    return {"id": str(conversation.id), "created_at": conversation.created_at}


@router.get("/{conversation_id}/messages")
async def get_messages(
    conversation_id: UUID,
    current_user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):
    conversation = await get_conversation(session, conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    messages = await get_conversation_messages(session, conversation_id)
    return [
        {
            "id": str(msg.id),
            "role": msg.role.value,
            "content": msg.content,
            "created_at": msg.created_at,
        }
        for msg in messages
    ]


@router.post("/{conversation_id}/message")
async def stream_message(
    conversation_id: UUID,
    chat_request: ChatRequest,
    current_user: UserResponse = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
):

    conversation = await get_conversation(session, conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    if conversation.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized",
        )

    await add_message(session, conversation_id, MessageRole.user, chat_request.message)

    history = await get_conversation_messages(session, conversation_id)
    messages = [
        {"role": msg.role.value, "content": msg.content}
        for msg in history
    ]

    async def stream_response():
        full_response = ""
        assistant_message_content = ""
        try:
            async for event_json in agent.run_stream(messages):
                # 事件已经是 JSON 格式，直接作为 JSON Lines 返回
                yield f"{event_json}\n"

                # 收集响应内容用于数据库存储
                try:
                    event = json.loads(event_json)
                    event_type = event.get("event")
                    event_data = event.get("data", {})

                    if event_type == "llm_stream" and event_data.get("content"):
                        assistant_message_content += event_data.get("content", "")
                    elif event_type == "agent_end" and event_data.get("output"):
                        if not assistant_message_content:
                            assistant_message_content = event_data.get("output", "")
                except (json.JSONDecodeError, AttributeError):
                    pass

            # 存储最终的助手消息
            if assistant_message_content:
                await add_message(session, conversation_id, MessageRole.assistant, assistant_message_content)
        except Exception as e:
            import traceback
            traceback.print_exc()
            yield json.dumps({
                "event": "error",
                "data": {"message": str(e)}
            }) + "\n"

    return StreamingResponse(stream_response(), media_type="text/event-stream")
