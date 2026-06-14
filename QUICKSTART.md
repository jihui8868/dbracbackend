# Quick Start Guide

Get the DBRCA Chat API running in 5 minutes.

## 1. Setup (2 min)
```bash
cd backend
uv sync
createdb dbrca
cp .env.example .env
```

## 2. Configure (1 min)
Edit `.env`:
```env
DATABASE_URL=postgresql+asyncpg://localhost/dbrca
SECRET_KEY=your-secret-key-here
DEEPSEEK_API_KEY=your-deepseek-key
```

## 3. Run (30 sec)
```bash
uv run uvicorn app.main:app --reload
```

Or with Python directly:
```bash
uv run python main.py
```

Visit: `http://localhost:8000/docs`

## 4. Test (1 min 30 sec)

### Register
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

### Login
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=testpass123" | jq -r '.access_token')
echo "Token: $TOKEN"
```

### Create Conversation
```bash
CONV_ID=$(curl -s -X POST http://localhost:8000/chat/sessions \
  -H "Authorization: Bearer $TOKEN" | jq -r '.id')
echo "Conversation ID: $CONV_ID"
```

### Chat (Streaming)
```bash
curl -X POST http://localhost:8000/chat/$CONV_ID/message \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, what is your name?"}' \
  -N  # Enable unbuffered streaming
```

## 5. Explore

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health

## Troubleshooting

**PostgreSQL connection error?**
- Install PostgreSQL: `brew install postgresql` (Mac) or `apt-get install postgresql` (Linux)
- Start it: `brew services start postgresql` or `sudo systemctl start postgresql`

**API key error?**
- Get DeepSeek key from: https://platform.deepseek.com
- Update `.env` with your key

**Module not found?**
- Run: `uv sync`

## Next Steps

- Read `README.md` for API reference
- Read `SETUP.md` for detailed setup
- Read `DEPLOYMENT_GUIDE.md` for production
- Edit `.env` for your DeepSeek API key
- Create frontend to use the API

---

That's it! You now have a working multi-agent chat API.
