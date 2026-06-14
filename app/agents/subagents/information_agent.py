"""
信息检索子代理 - 用于搜索和获取信息
"""
from typing import Annotated
from datetime import datetime

from langchain_core.tools import tool


@tool
def get_current_time() -> str:
    """获取当前日期和时间"""
    return str(datetime.now())


@tool
def web_search(query: str) -> str:
    """
    在网络上搜索信息

    Args:
        query: 搜索查询文本

    Returns:
        搜索结果摘要
    """
    # 实际实现中可以集成真实的搜索引擎 API
    return f"搜索 '{query}' 的结果: 这是一个占位符响应。在实际应用中，这里会调用真实的搜索 API (如 Google、Bing 等)。"


@tool
def get_weather(location: str) -> str:
    """
    获取指定位置的天气信息

    Args:
        location: 位置名称或城市名

    Returns:
        天气信息
    """
    # 实际实现中可以集成天气 API
    return f"{location} 的天气信息: 晴天，温度 25°C (占位符数据)"


# 信息代理的工具列表
INFORMATION_TOOLS = [
    get_current_time,
    web_search,
    get_weather,
]
