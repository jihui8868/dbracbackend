"""
实用工具子代理 - 用于文本处理、格式化等通用任务
"""
import hashlib
import json

from langchain_core.tools import tool


@tool
def text_processing(text: str, operation: str = "analyze") -> str:
    """
    处理和分析文本

    Args:
        text: 输入文本
        operation: 操作类型 ('analyze', 'summarize', 'translate')

    Returns:
        处理结果
    """
    if operation == "analyze":
        return f"文本分析:\n- 长度: {len(text)} 字符\n- 单词数: {len(text.split())}\n- 行数: {len(text.splitlines())}"
    elif operation == "summarize":
        # 简单的摘要实现 - 取前几句
        sentences = text.split("。")
        summary = "。".join(sentences[:2]) + "。" if sentences else text[:100]
        return f"摘要: {summary}"
    elif operation == "translate":
        return f"文本翻译 (占位符): 将文本从一种语言翻译到另一种语言"
    else:
        return f"未知的操作: {operation}"


@tool
def format_data(data: str, format_type: str = "json") -> str:
    """
    格式化数据

    Args:
        data: 数据字符串
        format_type: 目标格式 ('json', 'csv', 'xml')

    Returns:
        格式化后的数据
    """
    try:
        if format_type == "json":
            # 尝试解析并重新格式化为 JSON
            try:
                parsed = json.loads(data)
                return json.dumps(parsed, indent=2, ensure_ascii=False)
            except:
                return json.dumps({"data": data}, indent=2, ensure_ascii=False)
        elif format_type == "csv":
            lines = data.split("\n")
            csv_data = ",".join([f'"{line}"' for line in lines if line])
            return csv_data
        elif format_type == "xml":
            return f"<?xml version='1.0'?>\n<data>{data}</data>"
        else:
            return f"不支持的格式: {format_type}"
    except Exception as e:
        return f"格式化失败: {str(e)}"


@tool
def hash_data(data: str, algorithm: str = "sha256") -> str:
    """
    对数据进行哈希处理

    Args:
        data: 要哈希的数据
        algorithm: 哈希算法 ('md5', 'sha1', 'sha256')

    Returns:
        哈希值
    """
    algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
    }

    if algorithm not in algorithms:
        return f"不支持的算法: {algorithm}"

    hash_obj = algorithms[algorithm](data.encode())
    return f"{algorithm.upper()}: {hash_obj.hexdigest()}"


@tool
def validate_format(data: str, format_type: str) -> str:
    """
    验证数据格式

    Args:
        data: 数据字符串
        format_type: 预期格式 ('json', 'email', 'url', 'phone')

    Returns:
        验证结果
    """
    import re

    if format_type == "json":
        try:
            json.loads(data)
            return "✓ 有效的 JSON 格式"
        except:
            return "✗ 无效的 JSON 格式"
    elif format_type == "email":
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        is_valid = re.match(email_pattern, data)
        return "✓ 有效的电子邮件格式" if is_valid else "✗ 无效的电子邮件格式"
    elif format_type == "url":
        url_pattern = r"^https?://[^\s/$.?#].[^\s]*$"
        is_valid = re.match(url_pattern, data)
        return "✓ 有效的 URL 格式" if is_valid else "✗ 无效的 URL 格式"
    elif format_type == "phone":
        phone_pattern = r"^[\d\-\+\(\)\s]{7,}$"
        is_valid = re.match(phone_pattern, data)
        return "✓ 有效的电话号码格式" if is_valid else "✗ 无效的电话号码格式"
    else:
        return f"不支持的格式验证: {format_type}"


# 实用代理的工具列表
UTILITY_TOOLS = [
    text_processing,
    format_data,
    hash_data,
    validate_format,
]
