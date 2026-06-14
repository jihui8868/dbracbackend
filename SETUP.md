# FastAPI Chat Application Setup

## Prerequisites

- Python 3.13+
- PostgreSQL 12+
- uv (Python package manager)

## Installation

1. Install dependencies:
```bash
cd backend
uv sync
```

2. Set up environment variables:
   - Copy `.env.example` to `.env` or create `.env` with your settings:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbrca
   SECRET_KEY=your-random-secret-key
   DEEPSEEK_API_KEY=your-deepseek-api-key
   DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
   DEEPSEEK_MODEL=deepseek-chat
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

3. Create PostgreSQL database:
   ```bash
   createdb dbrca
   ```

## Running the Application

Start the development server:
```bash
cd backend
uv run uvicorn app.main:app --reload
```

Or with Python directly:
```bash
uv run python main.py
```

The API will be available at `http://localhost:8000`.

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user profile

### Chat
- `GET /chat/sessions` - List user's conversations
- `POST /chat/sessions` - Create new conversation
- `POST /chat/{conversation_id}/message` - Send message and stream response (SSE)

## Testing Endpoints

### Register User
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"username":"testuser","email":"test@example.com","password":"testpass"}'
```

### Login
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass"
```

### Create Conversation
```bash
curl -X POST http://localhost:8000/chat/sessions \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### Send Message (Streaming)
```bash
curl -X POST http://localhost:8000/chat/{conversation_id}/message \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message":"Hello, how are you?"}'
```

## Project Structure

```
backend/
├── main.py                 # FastAPI app entry point
├── .env                    # Environment variables
├── app/
│   ├── core/
│   │   ├── config.py       # Configuration (Pydantic Settings)
│   │   └── database.py     # SQLAlchemy setup
│   ├── models/
│   │   ├── user.py         # User ORM model
│   │   └── conversation.py # Conversation & Message models
│   ├── schemas/
│   │   ├── user.py         # User Pydantic schemas
│   │   └── chat.py         # Chat Pydantic schemas
│   ├── crud/
│   │   ├── user.py         # User database operations
│   │   └── conversation.py # Conversation database operations
│   ├── router/
│   │   ├── auth.py         # Authentication endpoints
│   │   └── chat.py         # Chat endpoints
│   └── agents/
│       ├── main_agent.py   # Main chat agent (DeepSeek)
│       └── subagents/
│           └── tools.py    # Agent tools definitions
```

## Key Features

- ✅ User authentication with JWT tokens
- ✅ Multi-turn conversations with session management
- ✅ Streaming responses (Server-Sent Events)
- ✅ PostgreSQL persistence
- ✅ DeepSeek LLM integration via OpenAI-compatible API
- ✅ Tool-calling support for agents
- ✅ CORS enabled for frontend integration
