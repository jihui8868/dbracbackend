# DeepAgent 实现文档

## 概述

本项目现已采用 **LangChain DeepAgent** (`deepagents` 库) 来创建多层级的代理系统。主代理可以协调多个专门的子代理，每个子代理处理特定的任务领域。

## 架构

```
┌─────────────────────────────────────────────┐
│         主代理 (DeepChatAgent)              │
│   使用 deepagents.create_deep_agent 创建   │
├─────────────────────────────────────────────┤
│                                             │
├──────────────────┬──────────────────┬──────┤
│  信息检索子代理   │  数据分析子代理   │ 代码 │
│  (Information    │  (Analysis       │ 生成 │
│   Agent)         │   Agent)         │ 子代 │
│                  │                  │ 理   │
├──────────┬───────┴──────────┬───────┴──────┤
│  工具函数子代理              │               │
│  (Utility Agent)            │               │
└─────────────────────────────┴───────────────┘
```

## 组件结构

### 1. 主代理 (`app/agents/main_agent.py`)

- **类**: `DeepChatAgent`
- **用途**: 使用 `deepagents.create_deep_agent` 创建高级代理
- **功能**:
  - 协调多个子代理
  - 理解用户请求
  - 选择合适的工具
  - 生成流式响应

```python
from deepagents import create_deep_agent
from langchain_openai import ChatOpenAI

agent = create_deep_agent(
    model=llm,
    tools=ALL_TOOLS,
    system_prompt="...",
)
```

### 2. 子代理系统

#### 2.1 信息检索子代理 (`app/agents/subagents/information_agent.py`)

**工具列表**:
- `get_current_time()` - 获取当前日期时间
- `web_search(query)` - 网络搜索
- `get_weather(location)` - 获取天气信息

**用途**: 处理所有信息检索相关的请求

#### 2.2 数据分析子代理 (`app/agents/subagents/analysis_agent.py`)

**工具列表**:
- `analyze_data(data, analysis_type)` - 分析数据
- `calculate_statistics(numbers)` - 计算统计信息
- `data_aggregation(data_sources)` - 聚合数据源

**用途**: 处理数据分析和统计计算

#### 2.3 代码生成子代理 (`app/agents/subagents/code_agent.py`)

**工具列表**:
- `generate_code(language, description)` - 生成代码
- `debug_code(code, error_message)` - 调试代码
- `code_review(code, aspects)` - 代码审查

**用途**: 处理代码相关的任务

#### 2.4 实用工具子代理 (`app/agents/subagents/utility_agent.py`)

**工具列表**:
- `text_processing(text, operation)` - 文本处理
- `format_data(data, format_type)` - 数据格式化
- `hash_data(data, algorithm)` - 数据哈希
- `validate_format(data, format_type)` - 格式验证

**用途**: 处理文本、格式和验证相关的任务

### 3. 工具集成

所有子代理的工具都集成在 `app/agents/subagents/__init__.py`:

```python
ALL_TOOLS = (
    INFORMATION_TOOLS +
    ANALYSIS_TOOLS +
    CODE_TOOLS +
    UTILITY_TOOLS
)
```

## 使用示例

### 1. 信息检索请求

**用户**: "今天的天气怎么样？"

流程:
1. 主代理接收请求
2. 识别这是一个信息检索任务
3. 调用 `get_weather()` 工具
4. 返回天气信息

### 2. 数据分析请求

**用户**: "分析这些数字的统计特性: [1, 2, 3, 4, 5]"

流程:
1. 主代理接收请求
2. 识别这是一个数据分析任务
3. 调用 `calculate_statistics()` 工具
4. 返回统计结果

### 3. 代码生成请求

**用户**: "用 Python 写一个计算阶乘的函数"

流程:
1. 主代理接收请求
2. 识别这是一个代码生成任务
3. 调用 `generate_code()` 工具
4. 返回生成的代码

## 依赖配置

在 `pyproject.toml` 中添加了以下依赖:

```toml
dependencies = [
    ...
    "deepagents>=0.6.10",
    "langchain>=0.3.0",
    "langchain-openai>=1.3.2",
    "langchain-core>=0.3.0",
    ...
]
```

## 扩展指南

### 添加新的子代理

1. 在 `app/agents/subagents/` 目录创建新的 Python 文件
2. 使用 `@tool` 装饰器定义工具函数
3. 创建 `TOOLS` 列表导出所有工具
4. 在 `__init__.py` 中导入并合并到 `ALL_TOOLS`

示例:

```python
# app/agents/subagents/custom_agent.py

from langchain_core.tools import tool

@tool
def my_custom_tool(param: str) -> str:
    """工具描述"""
    return f"处理结果: {param}"

CUSTOM_TOOLS = [my_custom_tool]
```

### 自定义主代理行为

修改 `app/agents/main_agent.py` 中的 `system_prompt`:

```python
system_prompt = """你是一个自定义 AI 助手...
你的特殊能力包括:
- ...
"""
```

## 工具调用流程

```
用户消息
  ↓
主代理接收
  ↓
理解意图并选择工具
  ↓
调用相应的工具函数
  ↓
获取工具执行结果
  ↓
生成响应
  ↓
流式返回给用户
```

## 性能优化

1. **异步处理**: 所有工具支持异步执行
2. **流式响应**: 支持实时流式返回结果
3. **工具缓存**: 可以缓存常用工具的结果
4. **并发调用**: 支持多个工具的并发执行

## 故障处理

- 工具执行失败时，代理会捕获异常并返回错误信息
- 支持重试机制和降级策略
- 详细的错误日志便于调试

## 监控和日志

主代理支持调试模式:

```python
agent = create_deep_agent(
    model=llm,
    tools=ALL_TOOLS,
    debug=True,  # 启用调试
)
```

## 未来改进

1. **更多子代理**: 添加数据库查询、API 集成等子代理
2. **子代理间协作**: 实现子代理间的通信和协作
3. **学习和优化**: 记录用户反馈，优化工具选择
4. **安全沙箱**: 使用安全的沙箱环境执行代码
5. **持久化**: 保存代理执行历史用于分析

## 参考资源

- [DeepAgents 文档](https://github.com/langchain-ai/deepagents)
- [LangChain 文档](https://python.langchain.com/)
- [OpenAI API 兼容接口](https://platform.openai.com/docs/api-reference)
