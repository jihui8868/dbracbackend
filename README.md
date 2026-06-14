# DBRCA Chat API

A production-ready FastAPI backend for multi-agent chat applications powered by DeepSeek LLM. Features include user authentication, multi-turn conversations, streaming responses, and tool-calling via agents.

## Quick Start

### Prerequisites
- Python 3.13+
- PostgreSQL 12+
- uv (Python package manager)

### Setup

1. **Navigate to the project:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   uv sync
   ```

3. **Set up PostgreSQL database:**
   ```bash
   createdb dbrca
   ```

4. **Create .env file:**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```
   
   Required environment variables:
   - `DATABASE_URL` - PostgreSQL connection string
   - `SECRET_KEY` - JWT signing key (use a strong random string)
   - `DEEPSEEK_API_KEY` - Your DeepSeek API key
   - `DEEPSEEK_BASE_URL` - Default: `https://api.deepseek.com/v1`
   - `DEEPSEEK_MODEL` - Default: `deepseek-chat`

5. **Run the development server:**
   ```bash
   uv run uvicorn app.main:app --reload
   ```

   Or with Python directly:
   ```bash
   uv run python main.py
   ```

The API will be available at `http://localhost:8000`

## API Documentation

### Interactive Docs
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

### Authentication Endpoints

#### Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "securepassword"
  }'
```

Response:
```json
{
  "id": "uuid",
  "username": "testuser",
  "email": "test@example.com",
  "created_at": "2024-01-01T12:00:00"
}
```

#### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=securepassword"
```

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

#### Get Current User
```bash
curl -X GET http://localhost:8000/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Chat Endpoints

All chat endpoints require `Authorization: Bearer TOKEN` header.

#### List Conversations
```bash
curl -X GET http://localhost:8000/chat/sessions \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

#### Create Conversation
```bash
curl -X POST http://localhost:8000/chat/sessions \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

Response:
```json
{
  "id": "conversation-uuid",
  "created_at": "2024-01-01T12:00:00"
}
```

#### Send Message (Streaming)
```bash
curl -X POST http://localhost:8000/chat/{conversation_id}/message \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, how can you help?"}'
```

This endpoint returns Server-Sent Events (SSE) with streaming response chunks:
```
data: {"type":"text","content":"Hello! I'm"}
data: {"type":"text","content":" happy to help"}
data: {"type":"done","content":""}
```

## Project Structure

```
backend/
├── main.py                      # Entry point (imports from app.main)
├── .env                         # Environment variables
├── .env.example                 # Example environment file
├── SETUP.md                     # Detailed setup instructions
├── pyproject.toml               # Project dependencies
└── app/
    ├── __init__.py
    ├── main.py                  # FastAPI app initialization
    ├── core/
    │   ├── config.py           # Configuration (Pydantic Settings)
    │   └── database.py         # SQLAlchemy async setup
    ├── models/
    │   ├── user.py             # User ORM model
    │   └── conversation.py     # Conversation & Message models
    ├── schemas/
    │   ├── user.py             # User request/response schemas
    │   └── chat.py             # Chat request/response schemas
    ├── crud/
    │   ├── user.py             # User database operations
    │   └── conversation.py     # Conversation/message DB operations
    ├── router/
    │   ├── auth.py             # Authentication endpoints
    │   └── chat.py             # Chat endpoints with streaming
    └── agents/
        ├── main_agent.py       # Main chat agent (DeepSeek integration)
        └── subagents/
            └── tools.py        # Agent tool definitions
```

## Database Schema

### Users Table
- `id` (UUID, PK)
- `username` (String, unique)
- `email` (String, unique)
- `hashed_password` (String)
- `created_at` (DateTime)

### Conversations Table
- `id` (UUID, PK)
- `user_id` (UUID, FK→users)
- `title` (String, nullable)
- `created_at` (DateTime)

### Messages Table
- `id` (UUID, PK)
- `conversation_id` (UUID, FK→conversations)
- `role` (Enum: user/assistant/tool)
- `content` (Text)
- `tool_calls` (JSON, nullable)
- `created_at` (DateTime)

## Features

✅ **User Authentication**
- JWT token-based authentication
- Password hashing with bcrypt
- User registration and login

✅ **Multi-turn Conversations**
- Session management with conversation IDs
- Full message history persistence
- Support for user, assistant, and tool roles

✅ **Streaming Responses**
- Server-Sent Events (SSE) for real-time response streaming
- Token-by-token response delivery

✅ **DeepSeek LLM Integration**
- OpenAI-compatible API interface
- Tool calling support for agents
- Configurable model and parameters

✅ **Database**
- PostgreSQL with async SQLAlchemy ORM
- Automatic table creation on startup
- Connection pooling

✅ **API Features**
- CORS enabled for frontend integration
- Automatic API documentation (Swagger/ReDoc)
- Request validation with Pydantic

## Development

### Adding a New Tool

Edit `app/agents/subagents/tools.py`:

```python
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "your_tool_name",
            "description": "Description of what the tool does",
            "parameters": {
                "type": "object",
                "properties": {
                    "param_name": {
                        "type": "string",
                        "description": "Parameter description"
                    }
                },
                "required": ["param_name"],
            },
        },
    },
]

async def execute_tool(tool_name: str, tool_input: dict) -> str:
    if tool_name == "your_tool_name":
        param = tool_input.get("param_name")
        # Implement your tool logic
        return "result"
```

### Testing with curl

See API Documentation section above for example requests.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `DATABASE_URL` | - | PostgreSQL connection string (required) |
| `SECRET_KEY` | - | JWT signing key (required) |
| `DEEPSEEK_API_KEY` | - | DeepSeek API key (required) |
| `DEEPSEEK_BASE_URL` | `https://api.deepseek.com/v1` | DeepSeek API endpoint |
| `DEEPSEEK_MODEL` | `deepseek-chat` | LLM model to use |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | JWT token expiration time |

## Troubleshooting

### Database Connection Error
- Verify PostgreSQL is running
- Check `DATABASE_URL` in .env
- Ensure database exists: `createdb dbrca`

### Import Errors
- Make sure dependencies are installed: `uv sync`
- Check that you're using the virtual environment: `uv run ...`

### CORS Issues
- CORS is enabled for all origins by default
- Modify in `main.py` if needed

## Production Deployment

Before deploying to production:

1. **Set strong SECRET_KEY:**
   ```bash
   python -c "import secrets; print(secrets.token_urlsafe(32))"
   ```

2. **Update CORS settings** in `main.py` with specific frontend URL

3. **Use a production ASGI server** (gunicorn, uvicorn with workers, etc.):
   ```bash
   uv run gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app
   ```

4. **Set up proper logging and monitoring**

5. **Use environment-specific secrets management**

## License

MIT
