from typing import AsyncIterator

from openai import AsyncOpenAI

from app.core.config import settings
from app.agents.subagents.tools import TOOLS, execute_tool
from app.models.conversation import MessageRole


class ChatAgent:
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
        )
        self.model = settings.DEEPSEEK_MODEL

    async def run_stream(
        self, messages: list[dict], tools: list[dict] | None = None
    ) -> AsyncIterator[str]:
        if tools is None:
            tools = TOOLS

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            stream=True,
        )

        async for chunk in response:
            if chunk.choices and chunk.choices[0].delta:
                delta = chunk.choices[0].delta
                if delta.content:
                    yield delta.content


agent = ChatAgent()
