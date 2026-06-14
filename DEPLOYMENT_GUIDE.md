# Deployment Guide - DBRCA Chat API

## Prerequisites

- Python 3.13+
- PostgreSQL 12+
- uv (Python package manager)

## Local Development Setup

### 1. Install Dependencies
```bash
cd backend
uv sync
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings
```

**Essential environment variables:**
```env
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbrca
SECRET_KEY=<generate-with: python -c "import secrets; print(secrets.token_urlsafe(32))">
DEEPSEEK_API_KEY=sk-<your-deepseek-api-key>
```

### 3. Create Database
```bash
createdb dbrca
```

### 4. Start Development Server
```bash
uv run uvicorn app.main:app --reload
```

Or with Python directly:
```bash
uv run python main.py
```

Server runs at `http://localhost:8000`

## Production Deployment

### 1. Generate Strong Secret Key
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 2. Set Production Environment Variables
```env
DATABASE_URL=postgresql+asyncpg://prod_user:strong_password@db.example.com:5432/dbrca
SECRET_KEY=<generated-secret-key>
DEEPSEEK_API_KEY=sk-<your-key>
ACCESS_TOKEN_EXPIRE_MINUTES=120
```

### 3. Update CORS Settings
Edit `main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-domain.com"],  # Specific domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 4. Use Production ASGI Server

#### Option A: Gunicorn with Uvicorn Workers
```bash
pip install gunicorn
uv run gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app
```

#### Option B: Uvicorn with Multiple Workers
```bash
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### 5. Set Up Reverse Proxy (Nginx)
```nginx
upstream fastapi {
    server 127.0.0.1:8000;
}

server {
    listen 80;
    server_name api.example.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://fastapi;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # For streaming responses
    location /chat {
        proxy_pass http://fastapi;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        
        # Enable streaming
        proxy_buffering off;
        proxy_request_buffering off;
    }
}
```

### 6. Set Up SSL/TLS (Let's Encrypt)
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --nginx -d api.example.com
```

Update Nginx to use SSL certificates.

### 7. Process Manager (Systemd)
Create `/etc/systemd/system/dbrca.service`:
```ini
[Unit]
Description=DBRCA Chat API
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/opt/dbrca/backend
Environment="PATH=/opt/dbrca/backend/.venv/bin"
ExecStart=/opt/dbrca/backend/.venv/bin/gunicorn \
    -w 4 \
    -k uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    --access-logfile - \
    --error-logfile - \
    app.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable dbrca
sudo systemctl start dbrca
sudo systemctl status dbrca
```

## Database Migrations

### Initial Setup
The application automatically creates all tables on startup via the lifespan context manager.

### Future Migrations
For schema changes, use Alembic:

```bash
# Generate migration
uv run alembic revision --autogenerate -m "Add column"

# Apply migration
uv run alembic upgrade head
```

## Monitoring & Logging

### Application Logs
```bash
# View recent logs
sudo journalctl -u dbrca -f

# View logs from specific time
sudo journalctl -u dbrca --since "2 hours ago"
```

### Database Connection Monitoring
```bash
# Check PostgreSQL connections
sudo -u postgres psql -c "SELECT datname, count(*) FROM pg_stat_activity GROUP BY datname;"
```

### Health Check
```bash
curl http://localhost:8000/health
```

## Backup & Recovery

### Database Backup
```bash
pg_dump dbrca > dbrca_backup.sql
```

### Database Restore
```bash
psql dbrca < dbrca_backup.sql
```

### Regular Backup (Cron)
Add to crontab:
```bash
0 2 * * * pg_dump dbrca | gzip > /backups/dbrca_$(date +\%Y\%m\%d).sql.gz
```

## Performance Tuning

### Database Pool Configuration
Edit `app/core/database.py`:
```python
engine = create_async_engine(
    settings.DATABASE_URL,
    pool_size=20,              # Number of connections to keep
    max_overflow=10,           # Additional connections when needed
    pool_pre_ping=True,        # Test connections before use
)
```

### Connection Limits in PostgreSQL
```sql
ALTER USER dbrca WITH CONNECTION LIMIT 100;
ALTER DATABASE dbrca WITH CONNECTION LIMIT 500;
```

## Security Checklist

- [ ] Strong SECRET_KEY generated
- [ ] DATABASE_URL uses environment variable
- [ ] DEEPSEEK_API_KEY kept secure
- [ ] CORS limited to specific frontend domain
- [ ] SSL/TLS enabled
- [ ] Database backups configured
- [ ] Logging enabled and monitored
- [ ] Rate limiting configured (if needed)
- [ ] Input validation verified
- [ ] SQL injection protection (SQLAlchemy ORM)
- [ ] XSS protection (Pydantic validation)
- [ ] CSRF protection (if needed for forms)

## Troubleshooting

### 502 Bad Gateway
- Check if FastAPI app is running: `curl http://localhost:8000/health`
- Check Nginx logs: `tail -f /var/log/nginx/error.log`
- Check application logs: `journalctl -u dbrca -f`

### Database Connection Refused
- Verify PostgreSQL is running: `sudo systemctl status postgresql`
- Check DATABASE_URL connection string
- Verify user permissions: `psql -U user dbrca`

### Slow Responses
- Check database query performance: `EXPLAIN ANALYZE <query>`
- Monitor connection pool usage
- Check API response times in logs
- Verify network connectivity

### High Memory Usage
- Check for connection leaks
- Verify connection pool is being closed properly
- Monitor with: `ps aux | grep gunicorn`

## Rollback Procedures

### Revert to Previous Version
```bash
# Stop current version
sudo systemctl stop dbrca

# Switch to previous commit
git checkout previous-commit-hash

# Reinstall dependencies
uv sync

# Revert database if schema changed
# (Have backup ready)
psql dbrca < dbrca_backup_before_migration.sql

# Restart
sudo systemctl start dbrca
```

## Update Procedures

### Safe Update Process
1. Create database backup: `pg_dump dbrca > backup.sql`
2. Update code: `git pull origin main`
3. Update dependencies: `uv sync`
4. Restart service: `sudo systemctl restart dbrca`
5. Verify health: `curl http://localhost:8000/health`
6. Monitor logs: `journalctl -u dbrca -f`

## Support & Documentation

- API Documentation: `http://your-domain/docs`
- README: See `README.md`
- Setup Guide: See `SETUP.md`

---

**Last Updated:** 2026-06-14
