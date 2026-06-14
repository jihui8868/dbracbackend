"""
子代理模块 - 包含不同功能的子代理
"""

from app.agents.subagents.information_agent import INFORMATION_TOOLS
from app.agents.subagents.analysis_agent import ANALYSIS_TOOLS
from app.agents.subagents.code_agent import CODE_TOOLS
from app.agents.subagents.utility_agent import UTILITY_TOOLS

# 合并所有工具
ALL_TOOLS = INFORMATION_TOOLS + ANALYSIS_TOOLS + CODE_TOOLS + UTILITY_TOOLS

__all__ = [
    "INFORMATION_TOOLS",
    "ANALYSIS_TOOLS",
    "CODE_TOOLS",
    "UTILITY_TOOLS",
    "ALL_TOOLS",
]
