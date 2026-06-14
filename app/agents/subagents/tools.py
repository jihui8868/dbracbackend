from datetime import datetime


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "Get the current date and time",
            "parameters": {
                "type": "object",
                "properties": {},
                "required": [],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query",
                    }
                },
                "required": ["query"],
            },
        },
    },
]


async def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "get_current_time":
        return str(datetime.now())
    elif tool_name == "web_search":
        query = tool_input.get("query", "")
        return f"Search results for: {query} (placeholder)"
    else:
        return f"Tool {tool_name} not found"
