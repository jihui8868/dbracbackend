# DeepAgent 快速参考指南

## 🎯 快速开始

### 1. 启动后端
```bash
cd backend
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 2. 发送消息到代理
```bash
curl -X POST http://localhost:8000/chat/{conversation_id}/message \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"message": "你的问题"}'
```

## 📂 文件结构速查

```
app/agents/
├── main_agent.py                 # 主代理 (DeepChatAgent)
└── subagents/
    ├── __init__.py              # 工具集合
    ├── information_agent.py      # 信息检索 (3 个工具)
    ├── analysis_agent.py         # 数据分析 (3 个工具)
    ├── code_agent.py             # 代码生成 (3 个工具)
    └── utility_agent.py          # 工具函数 (4 个工具)
```

## 🛠️ 工具速查表

### 信息检索工具
| 工具 | 参数 | 返回值 |
|------|------|--------|
| `get_current_time()` | 无 | 当前日期时间 |
| `web_search(query)` | query: str | 搜索结果 |
| `get_weather(location)` | location: str | 天气信息 |

### 数据分析工具
| 工具 | 参数 | 返回值 |
|------|------|--------|
| `analyze_data(data, type)` | data: str, type: str | 分析结果 |
| `calculate_statistics(nums)` | nums: list[float] | 统计数据 |
| `data_aggregation(sources)` | sources: list[str] | 聚合结果 |

### 代码生成工具
| 工具 | 参数 | 返回值 |
|------|------|--------|
| `generate_code(lang, desc)` | lang: str, desc: str | 代码片段 |
| `debug_code(code, error)` | code: str, error: str | 调试建议 |
| `code_review(code, aspects)` | code: str, aspects: str | 审查结果 |

### 实用工具
| 工具 | 参数 | 返回值 |
|------|------|--------|
| `text_processing(text, op)` | text: str, op: str | 处理结果 |
| `format_data(data, fmt)` | data: str, fmt: str | 格式化数据 |
| `hash_data(data, algo)` | data: str, algo: str | 哈希值 |
| `validate_format(data, fmt)` | data: str, fmt: str | 验证结果 |

## 💬 常见用户请求示例

### 信息类
- "现在几点了？" → `get_current_time()`
- "搜索 Python 教程" → `web_search()`
- "北京的天气怎样？" → `get_weather()`

### 分析类
- "分析这些数据" → `analyze_data()`
- "计算平均值" → `calculate_statistics()`
- "合并多个数据源" → `data_aggregation()`

### 代码类
- "写一个 Python 函数" → `generate_code()`
- "调试这个代码" → `debug_code()`
- "审查代码质量" → `code_review()`

### 工具类
- "处理这个文本" → `text_processing()`
- "格式化为 JSON" → `format_data()`
- "计算哈希值" → `hash_data()`
- "验证电子邮件" → `validate_format()`

## 🔧 常见操作

### 添加新工具
```python
# 1. 创建工具
from langchain_core.tools import tool

@tool
def my_tool(param: str) -> str:
    """工具说明"""
    return f"结果: {param}"

# 2. 导出工具列表
MY_TOOLS = [my_tool]

# 3. 在 __init__.py 中注册
from .my_agent import MY_TOOLS
ALL_TOOLS = [...] + MY_TOOLS
```

### 修改系统提示
```python
# 在 main_agent.py 中修改 system_prompt
system_prompt = """你是一个自定义助手...
新的指令...
"""
```

### 调试代理执行
```python
# 启用调试模式
agent = create_deep_agent(
    model=llm,
    tools=ALL_TOOLS,
    debug=True,  # 启用调试
)
```

## 📊 常用工具参数

### text_processing 操作类型
- `"analyze"` - 分析文本
- `"summarize"` - 总结文本
- `"translate"` - 翻译文本

### format_data 格式类型
- `"json"` - JSON 格式
- `"csv"` - CSV 格式
- `"xml"` - XML 格式

### hash_data 算法
- `"md5"` - MD5 哈希
- `"sha1"` - SHA1 哈希
- `"sha256"` - SHA256 哈希

### validate_format 格式验证
- `"json"` - JSON 格式
- `"email"` - 电子邮件
- `"url"` - URL 地址
- `"phone"` - 电话号码

## 🐛 调试技巧

### 查看所有可用工具
```python
from app.agents.subagents import ALL_TOOLS
for tool in ALL_TOOLS:
    print(f"{tool.name}: {tool.description}")
```

### 测试单个工具
```python
from app.agents.subagents.information_agent import get_current_time
result = get_current_time.invoke({})
print(result)
```

### 查看代理执行日志
```bash
# 查看后端日志
tail -f /tmp/backend.log
```

## ⚡ 性能优化

### 缓存结果
- 经常使用的工具结果可缓存
- 减少重复计算

### 并发执行
- 多个工具可并发调用
- 加快处理速度

### 流式响应
- 实时返回部分结果
- 改善用户体验

## 🔐 安全最佳实践

- ✓ 始终验证用户输入
- ✓ 限制可执行的操作范围
- ✓ 记录所有工具调用
- ✓ 使用认证令牌保护 API
- ✓ 定期审查日志

## 📚 文档链接

- [完整实现文档](./DEEPAGENT_IMPLEMENTATION.md)
- [实现总结](./AGENT_IMPLEMENTATION_SUMMARY.md)
- [LangChain 官方文档](https://python.langchain.com/)
- [DeepAgents GitHub](https://github.com/langchain-ai/deepagents)

## 🆘 常见问题

### Q: 工具不被调用？
A: 检查工具说明是否清晰，确保 LLM 理解了工具的功能。

### Q: 响应很慢？
A: 可能是 LLM API 响应慢，检查网络连接和 API 配额。

### Q: 工具执行出错？
A: 查看错误日志，确保参数类型和值正确。

### Q: 如何添加新的子代理？
A: 参考 "添加新工具" 部分，创建新的代理文件。

## 📞 支持

遇到问题？检查：
1. 后端日志: `/tmp/backend.log`
2. 代理日志: 启用 `debug=True`
3. 工具定义: `app/agents/subagents/`
4. API 文档: `/docs` (Swagger UI)

---

**最后更新**: 2026-06-14
**版本**: 1.0.0
