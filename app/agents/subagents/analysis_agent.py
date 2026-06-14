"""
数据分析子代理 - 用于数据分析和统计
"""
from typing import Annotated
import json

from langchain_core.tools import tool


@tool
def analyze_data(data: str, analysis_type: str = "summary") -> str:
    """
    分析提供的数据

    Args:
        data: JSON 格式的数据
        analysis_type: 分析类型 ('summary', 'statistics', 'trends')

    Returns:
        分析结果
    """
    try:
        data_obj = json.loads(data) if isinstance(data, str) else data

        if analysis_type == "summary":
            return f"数据摘要: 包含 {len(data_obj) if isinstance(data_obj, (list, dict)) else 1} 个项目"
        elif analysis_type == "statistics":
            return "统计分析: 数据包含数值和分类信息 (占位符)"
        elif analysis_type == "trends":
            return "趋势分析: 识别数据中的关键趋势 (占位符)"
        else:
            return "未知的分析类型"
    except Exception as e:
        return f"分析失败: {str(e)}"


@tool
def calculate_statistics(numbers: list[float]) -> str:
    """
    计算统计信息

    Args:
        numbers: 数字列表

    Returns:
        统计结果 (平均值, 中位数, 标准差等)
    """
    if not numbers:
        return "数字列表为空"

    import statistics

    avg = statistics.mean(numbers)
    median = statistics.median(numbers)

    result = {
        "count": len(numbers),
        "mean": round(avg, 2),
        "median": median,
        "min": min(numbers),
        "max": max(numbers),
    }

    if len(numbers) > 1:
        result["stdev"] = round(statistics.stdev(numbers), 2)

    return json.dumps(result, ensure_ascii=False)


@tool
def data_aggregation(data_sources: list[str]) -> str:
    """
    聚合多个数据源

    Args:
        data_sources: 数据源列表

    Returns:
        聚合结果
    """
    return f"已聚合 {len(data_sources)} 个数据源: {', '.join(data_sources[:3])}..."


# 分析代理的工具列表
ANALYSIS_TOOLS = [
    analyze_data,
    calculate_statistics,
    data_aggregation,
]
