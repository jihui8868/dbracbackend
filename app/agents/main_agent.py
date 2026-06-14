"""
主代理 - 使用 deepagents 的 create_deep_agent
实现真正的事件流式处理
"""
import json
from typing import AsyncIterator

from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI

from app.core.config import settings
from app.agents.subagents import ALL_TOOLS


class DeepChatAgent:
    """
    深度聊天代理 - 使用 deepagents 的 create_deep_agent
    支持多层级的代理协调和工具调用
    实现真正的事件流式处理
    """

    def __init__(self):
        """初始化深度代理"""
        # 初始化 LLM 模型，启用流式
        self.llm = ChatOpenAI(
            model_name=settings.DEEPSEEK_MODEL,
            api_key=settings.DEEPSEEK_API_KEY,
            base_url=settings.DEEPSEEK_BASE_URL,
            temperature=0.7,
            max_tokens=2000,
            streaming=True,  # 启用流式
        )

        # 创建系统提示
        system_prompt = """你是一个功能强大的 AI 助手，由多个专门的子代理组成。
你可以访问以下功能：

1. **信息检索**：搜索网络信息、获取当前时间和天气
2. **数据分析**：分析数据、计算统计信息、聚合数据源
3. **代码生成**：生成代码、调试代码、审查代码质量
4. **工具函数**：文本处理、格式化数据、数据验证

当用户需要帮助时，根据他们的请求选择合适的工具。
尽量准确和有帮助地回答问题。"""

        # 使用 create_deep_agent 创建深度代理
        self.agent = create_deep_agent(
            model=self.llm,  # 传入 LLM 模型对象
            tools=ALL_TOOLS,  # 传入所有可用的工具
            system_prompt=system_prompt,  # 系统提示词
            debug=False,  # 调试模式
        )

    async def run_stream(
        self, messages: list[dict], tools: list = None
    ) -> AsyncIterator[str]:
        """
        流式运行代理 - 使用 LangChain 事件流

        参考: https://docs.langchain.com/oss/javascript/langchain/event-streaming

        Args:
            messages: 消息历史列表，每个消息是 {'role': 'user'|'assistant', 'content': '...'}
            tools: 可选的工具列表 (未使用，保持与旧接口的兼容性)

        Yields:
            流式事件 JSON 字符串，包括:
            - llm_start: LLM 开始处理
            - llm_stream: LLM 流式输出
            - tool_start: 工具开始执行
            - tool_end: 工具执行完成
            - agent_end: 代理完成
            - error: 错误发生
        """
        # 构建用户输入
        user_message = None
        for msg in reversed(messages):
            if msg.get("role") == "user":
                user_message = msg.get("content", "")
                break

        if not user_message:
            yield json.dumps(
                {
                    "event": "error",
                    "data": {"message": "没有找到用户消息"},
                }
            )
            return

        # 构建聊天历史上下文
        context = ""
        for msg in messages[:-1]:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            if role == "assistant":
                context += f"助手: {content}\n"
            else:
                context += f"用户: {content}\n"

        full_prompt = f"{context}用户: {user_message}" if context else user_message

        try:
            # 发送用户消息事件
            yield json.dumps(
                {
                    "event": "user_message",
                    "data": {"message": user_message},
                }
            )

            # 使用 astream_events 获取实时事件流
            # 这提供了真正的流式处理，而不是等待完整结果
            async for event in self.agent.astream_events(
                {"messages": [{"role": "user", "content": full_prompt}]},
                version="v1",  # 使用最新的事件版本
            ):
                event_type = event.get("event")
                data = event.get("data", {})

                # 处理不同类型的事件
                if event_type == "on_llm_start":
                    # LLM 开始处理
                    yield json.dumps(
                        {
                            "event": "llm_start",
                            "data": {
                                "message": "AI 开始思考...",
                                "run_id": event.get("run_id"),
                            },
                        }
                    )

                elif event_type == "on_llm_stream":
                    # LLM 流式输出 - 真正的流式内容
                    if "chunk" in data:
                        chunk = data["chunk"]
                        if hasattr(chunk, "content") and chunk.content:
                            yield json.dumps(
                                {
                                    "event": "llm_stream",
                                    "data": {
                                        "content": chunk.content,
                                        "run_id": event.get("run_id"),
                                    },
                                }
                            )

                elif event_type == "on_tool_start":
                    # 工具开始执行
                    tool_name = data.get("payload", {}).get("name", "unknown")
                    yield json.dumps(
                        {
                            "event": "tool_start",
                            "data": {
                                "tool": tool_name,
                                "message": f"正在执行工具: {tool_name}",
                                "run_id": event.get("run_id"),
                            },
                        }
                    )

                elif event_type == "on_tool_end":
                    # 工具执行完成
                    tool_name = data.get("payload", {}).get("name", "unknown")
                    tool_output = data.get("output", "")
                    yield json.dumps(
                        {
                            "event": "tool_end",
                            "data": {
                                "tool": tool_name,
                                "output": str(tool_output)[:500],  # 限制输出大小
                                "message": f"工具 {tool_name} 执行完成",
                                "run_id": event.get("run_id"),
                            },
                        }
                    )

                elif event_type == "on_agent_action":
                    # 代理采取行动
                    yield json.dumps(
                        {
                            "event": "agent_action",
                            "data": {
                                "message": "代理正在处理...",
                                "run_id": event.get("run_id"),
                            },
                        }
                    )

                elif event_type == "on_chain_end":
                    # 链/代理执行完成
                    output = data.get("output", "")
                    if output:
                        yield json.dumps(
                            {
                                "event": "agent_end",
                                "data": {
                                    "output": str(output),
                                    "message": "代理处理完成",
                                    "run_id": event.get("run_id"),
                                },
                            }
                        )

            # 发送完成信号
            yield json.dumps(
                {
                    "event": "done",
                    "data": {"message": "流式处理完成"},
                }
            )

        except Exception as e:
            error_msg = f"代理执行出错: {str(e)}"
            print(f"Error: {error_msg}")
            import traceback

            traceback.print_exc()

            yield json.dumps(
                {
                    "event": "error",
                    "data": {"message": error_msg},
                }
            )


# 创建全局代理实例
agent = DeepChatAgent()


# 为了保证向后兼容性，保留原来的接口
class ChatAgent:
    """兼容旧接口的聊天代理"""

    def __init__(self):
        self.agent = agent

    async def run_stream(
        self, messages: list[dict], tools: list = None
    ) -> AsyncIterator[str]:
        """运行聊天"""
        async for chunk in self.agent.run_stream(messages, tools):
            yield chunk


# 导出代理实例供路由使用
__all__ = ["agent", "DeepChatAgent", "ChatAgent"]
