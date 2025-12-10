# Deployment Guide - CDR Analyzer

## Quick Start (Development)

### Option 1: Manual Setup

#### Backend
```bash
cd cdr-analyzer/backend

# Windows
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python main.py
```

Backend will run on `http://localhost:8000`
API docs available at `http://localhost:8000/docs`

#### Frontend
```bash
cd cdr-analyzer/frontend

# Simple HTTP server
python -m http.server 8080
```

Frontend will be available at `http://localhost:8080`

### Option 2: Docker (Recommended for Production)

```bash
cd cdr-analyzer
docker-compose up -d
```

- Backend: `http://localhost:8000`
- Frontend: `http://localhost:8080`

## Testing

```bash
cd cdr-analyzer/backend
pip install -r requirements-dev.txt
pytest tests/ -v
```

## Production Deployment

### Requirements
- Python 3.10+
- 2GB RAM minimum
- 10GB disk space

### Environment Variables
```bash
export DATABASE_PATH=/path/to/cdr.db
export API_HOST=0.0.0.0
export API_PORT=8000
```

### Systemd Service (Linux)

Create `/etc/systemd/system/cdr-analyzer.service`:

```ini
[Unit]
Description=CDR Analyzer Backend
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/cdr-analyzer/backend
Environment="PATH=/opt/cdr-analyzer/backend/venv/bin"
ExecStart=/opt/cdr-analyzer/backend/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable cdr-analyzer
sudo systemctl start cdr-analyzer
```

### Nginx Configuration

```nginx
server {
    listen 80;
    server_name cdr-analyzer.example.com;

    # Frontend
    location / {
        root /opt/cdr-analyzer/frontend;
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Backend API
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # API Docs
    location /docs {
        proxy_pass http://localhost:8000/docs;
        proxy_set_header Host $host;
    }
}
```

## Performance Tuning

### Database Optimization
```sql
-- Run periodically to optimize database
VACUUM;
ANALYZE;
```

### Backup Strategy
```bash
# Backup database daily
sqlite3 cdr.db ".backup /backups/cdr-$(date +%Y%m%d).db"
```

## Monitoring

Check application logs:
```bash
# Development
tail -f backend/app.log

# Production (systemd)
journalctl -u cdr-analyzer -f
```

## Troubleshooting

### Database locked error
```bash
# Check for long-running queries
sqlite3 cdr.db "PRAGMA busy_timeout = 5000;"
```

### High memory usage
- Limit CSV file size to 10MB
- Consider processing in chunks for larger files

### Slow queries
- Ensure indexes are created (done automatically on init)
- Check query plans: `EXPLAIN QUERY PLAN SELECT ...`

## Security Checklist

- [ ] Enable HTTPS in production
- [ ] Implement authentication (future version)
- [ ] Set file upload limits
- [ ] Regular database backups
- [ ] Monitor disk space
- [ ] Update dependencies regularly

## Maintenance

### Update Application
```bash
cd cdr-analyzer
git pull
cd backend
pip install -r requirements.txt --upgrade
sudo systemctl restart cdr-analyzer
```

### Clear Old Data
```sql
-- Remove records older than 1 year
DELETE FROM call_records 
WHERE timestamp < datetime('now', '-1 year');
VACUUM;
```
