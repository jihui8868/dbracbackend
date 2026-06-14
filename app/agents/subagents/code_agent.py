"""
代码生成和执行子代理 - 用于代码相关任务
"""
import re

from langchain_core.tools import tool


@tool
def generate_code(language: str, description: str) -> str:
    """
    根据描述生成代码

    Args:
        language: 编程语言 (python, javascript, sql 等)
        description: 代码功能描述

    Returns:
        生成的代码片段
    """
    code_templates = {
        "python": f"""# {description}
def example_function():
    # 这是一个示例函数
    result = "Hello, World!"
    return result

if __name__ == "__main__":
    print(example_function())
""",
        "javascript": f"""// {description}
function exampleFunction() {{
    // 这是一个示例函数
    const result = "Hello, World!";
    return result;
}}

console.log(exampleFunction());
""",
        "sql": f"""-- {description}
SELECT * FROM users
WHERE status = 'active'
LIMIT 10;
""",
    }

    return code_templates.get(
        language.lower(),
        f"# {description}\n# 不支持的语言: {language}",
    )


@tool
def debug_code(code: str, error_message: str = "") -> str:
    """
    调试代码并提供修复建议

    Args:
        code: 代码片段
        error_message: 错误消息

    Returns:
        调试建议
    """
    suggestions = []

    if "import" in code and error_message:
        suggestions.append("检查导入语句是否正确")

    if "{" in code and code.count("{") != code.count("}"):
        suggestions.append("大括号不匹配")

    if "def " in code or "function " in code:
        suggestions.append("检查函数签名和缩进")

    if not suggestions:
        suggestions.append("代码看起来没有明显问题，请提供更具体的错误信息")

    return "调试建议:\n" + "\n".join(f"- {s}" for s in suggestions)


@tool
def code_review(code: str, aspects: str = "all") -> str:
    """
    审查代码质量

    Args:
        code: 代码片段
        aspects: 审查方面 ('readability', 'performance', 'security', 'all')

    Returns:
        代码审查结果
    """
    review_items = {
        "readability": "代码可读性: 使用清晰的变量名和函数名",
        "performance": "性能: 检查是否有不必要的循环或重复计算",
        "security": "安全性: 验证输入并避免注入漏洞",
    }

    if aspects == "all":
        return "代码审查结果:\n" + "\n".join(f"✓ {v}" for v in review_items.values())
    else:
        return review_items.get(aspects, "未知的审查方面")


# 代码代理的工具列表
CODE_TOOLS = [
    generate_code,
    debug_code,
    code_review,
]
